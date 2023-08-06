import re
from pprint import pprint
from copy import deepcopy
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import layers
from tensorflow.keras import activations
from . import load
from . import addons
import tfbox.utils.helpers as h
#
# CONSTANTS
#
DEFAULT_ACTIVATION='relu'
DEFAULT_DROPOUT=False
DEFAULT_DROPOUT_RATE=0.5
DEFAULT_MAX_POOLING={
    'pool_size': 3, 
    'strides': 2, 
    'padding': "same"
}
DEFAULT_GLOBAL_POOLING='average'
UPSAMPLE_ERROR=(
    'upsample called with scale==1. '
    'Use allow_identity=True to force.'
)
EPS=1e-8
#
# HELPERS
#
def get(key,activation=False):
    key=h.snake(key)
    if activation:
        act=ACTIVATIONS.get(key.lower())
        if not act:
            act=getattr(activations,h.camel(key))
        return act
    else:
        blk=BLOCKS.get(key)
        if not blk:
            blk=getattr(layers,h.camel(key))
        return blk


def layer_name(*name_path,index=None,named=True):
    if named and name_path:
        name_path=[p for p in name_path if p] 
        name='.'.join(name_path)
        if index is not None:
            name=f'{name}-{index}'
        return name


def get_activation(act,**config):
    if act:
        if act is True:
            act=DEFAULT_ACTIVATION
        if isinstance(act,str):
            act=get(act,activation=True)
        act=act(**config)
    return act


def upsample(
        x,
        scale=None,
        like=None,
        shape=None,
        rescale=1,
        mode='bilinear',
        allow_resize=True,
        force_resize=False,
        allow_identity=False):
    if scale is None:
        if shape is None:
            shape=like.shape
        scale=rescale*shape[2]/x.shape[2]
    if scale==1:
        if not allow_identity:
            raise ValueError(UPSAMPLE_ERROR)
    else:
        if allow_resize and (force_resize or (scale!=int(scale))):
            h=round(x.shape[1]*scale)
            w=round(x.shape[2]*scale)
            x=tf.image.resize(x,(h,w),method=mode)
        else:
            scale=int(scale)
            x=layers.UpSampling2D(
                size=(scale,scale),
                interpolation=mode)(x)
    return x



def build_block(config,btype=None,index=None):
    config=_config_dict(config)
    btype=config.pop('btype',btype or DEFAULT_BTYPE)
    name=config.get('name')
    if index and name:
        config['name']=f'{name}.{index}'
    return get(btype)(**config)


def build_blocks(config,indexed=True,singles_as_block=False):
    block_stack=[]
    config=_config_dict(config)
    layers=config.pop('layers',False)
    nb_repeats=config.pop('nb_repeats',False)
    if layers or nb_repeats:
        as_block=False
        layers=layers or [{}]
        nb_repeats=nb_repeats or 1
        for i in range(nb_repeats):
            for j,c in enumerate(layers):
                if indexed and (not as_block):
                    index=f'{i}-{j}'
                else:
                    index=None
                cfg=config.copy()
                cfg.update(_config_dict(c,cfg.get('btype')))
                block_stack.append(
                    build_block(cfg,index=index))
    else:
        as_block=singles_as_block
        block_stack.append(build_block(config))
    if as_block:
        return block_stack[0]
    else:
        return block_stack


def _config_dict(config,btype=None):
    if not config:
        config={}
    elif isinstance(config,str):
        config={
            'btype': config,
        }
    elif isinstance(config,int):
        config={
            'btype': btype or INT_BTYPE,
            'filters': config,
        }
    else:
        config=deepcopy(config)
        nb_keys=len(config)
        if nb_keys==1:
            key, value=next(iter(config.items()))
            if _valid_key(key):
                btype=key
                config=value
            else:
                btype= config.get('btype',btype) or DEFAULT_BTYPE
            config['btype']=btype
    return config


def _valid_key(key):
    key=h.snake(key)
    if key in list(BLOCKS.keys())+list(ACTIVATIONS.keys()):
        return True
    else:
        try:
            getattr(layers,h.camel(key))
            return True
        except:
            try:
                getattr(activations,h.camel(key))
                return True
            except:
                return False


#
# GENERAL BLOCKS 
#
class Conv(keras.Model):
    """ Conv-Norm-Activation-Dropout
    """
    BATCH_NORM='batch'
    GROUP_NORM='group'
    DEFAULT_NORM=BATCH_NORM
    DEFAULT_ORDER=['conv','act','norm','do']
    ACT_LAST_ORDER=['conv','norm','do','act']
    RES_ORDER=['norm','act','conv','do']
    #
    # PUBLIC
    #
    def __init__(self,
            filters=None,
            kernel_size=3,
            padding='same',
            seperable=False,
            pointwise_first=False,
            depthwise=False,
            norm=BATCH_NORM,
            norm_config={},
            act=True,
            act_config={},
            dilation_rate=1,
            strides=1,
            dropout=DEFAULT_DROPOUT,
            dropout_config={},
            act_last=False,
            order=DEFAULT_ORDER,
            is_skip=False,
            name=None,
            named_layers=True,
            **conv_config):
        super(Conv, self).__init__()
        self.paddings=False
        self.block_name=name or self.name
        self.named_layers=named_layers
        if dilation_rate>1:
            strides=1
        if kernel_size in [1,(1,1)]:
            dilation_rate=1
            if padding.lower() in ['reflect','symmetric']:
                padding='valid'
        elif padding and (padding.lower() in ['reflect','symmetric']):
            self.padding_mode=padding
            p=int(kernel_size//2)
            self.paddings=tf.constant([
                [0,0],
                [p,p],
                [p,p],
                [0,0]])
            padding='valid'
        _conv, cname, filters=self._conv_setup(depthwise,seperable,pointwise_first,filters)
        if filters:
            conv_config['filters']=filters
        self.conv=_conv(
            kernel_size=kernel_size,
            padding=padding,
            dilation_rate=dilation_rate,
            strides=strides,
            name=self._layer_name(cname),
            **conv_config)
        self.is_skip=is_skip
        if order=='res':
            self.order=Conv.RES_ORDER
        elif act_last or (order=='act_last'):
            self.order=Conv.ACT_LAST_ORDER
        elif isinstance(order,list):
            self.order=order
        else:
            self.order=Conv.DEFAULT_ORDER
        self.norm=self._norm(norm,norm_config)
        self.act=self._activation(act,act_config)
        self.do=self._dropout(dropout,dropout_config)


    def __call__(self,x):
        for m in self.order:
            l=getattr(self,m)
            if l: 
                if (self.paddings is not False) and (m=='conv'):
                    x=tf.pad(x,self.paddings,self.padding_mode)
                x=l(x)
        return x


    #
    # INTERNAL
    #
    def _conv_setup(self,depthwise,seperable,pointwise_first,filters):
        if depthwise:
            _conv=layers.DepthwiseConv2D
            cname='depthconv2d'
            filters=None
        else:
            if seperable:
                if pointwise_first:
                    _conv=XSeparableConv2D
                    cname='xsepconv2d'
                else:
                    _conv=layers.SeparableConv2D
                    cname='sepconv2d'
            else:
                _conv=layers.Conv2D
                cname='conv2d'
        return _conv, cname, filters



    def _layer_name(self,name):
        return layer_name(self.block_name,name,named=self.named_layers)


    def _norm(self,norm,norm_config):
        if norm==True:
            norm=Conv.DEFAULT_NORM
        if norm==Conv.BATCH_NORM:
            norm=layers.BatchNormalization(
                name=self._layer_name('batch_norm'),
                **norm_config)
        elif norm==Conv.GROUP_NORM:
            norm=addons.GroupNormalization(
                name=self._layer_name('group_norm'),
                **norm_config)
        elif norm:
            raise ValueError('only `group` and `batch` norms implemented')
        else:
            norm=False
        return norm      


    def _activation(self,act,config):
        if act:
            act=get_activation(act,name=self._layer_name('activation'),**config)
        return act


    def _dropout(self,dropout,config):
        if dropout:
            if dropout is True:
                dropout=DEFAULT_DROPOUT_RATE
            dropout=layers.Dropout(dropout,name=self._layer_name('dropout'),**config)
            return dropout



class XSeparableConv2D(keras.Model):
    """ Xception Style Seperable Conv (pointwise first)
    """
    #
    # PUBLIC
    #
    def __init__(self,filters,**conv_config):
        super(XSeparableConv2D, self).__init__()
        self.pointwise=layers.Conv2D(filters=filters,kernel_size=1)
        self.depthwise=layers.DepthwiseConv2D(**conv_config)

    def __call__(self,x):
        x=self.pointwise(x)
        return self.depthwise(x)


class BandMath(keras.Model):
    """ BandMath: Let the model learn band indices
    """
    DEFAULT_ORDER=['act','norm']
    BATCH_NORM='batch'
    GROUP_NORM='group'
    DEFAULT_NORM=BATCH_NORM
    #
    # PUBLIC
    #
    def __init__(self,filters,
            depth=1,
            norm=DEFAULT_NORM,
            norm_config={},
            act=True,
            act_config={},
            conv_act=False,
            conv_norm=False,
            name=None,
            order=DEFAULT_ORDER,
            **conv_config):
        super(BandMath, self).__init__()
        self.block_name=name or self.name
        self.numerator_stack=[
            Conv(
                filters=filters,
                kernel_size=1,
                act=conv_act,
                norm=conv_norm,
                name=layer_name(f'{self.block_name}_n',index=i),
                **conv_config)
            for i in range(depth)]
        self.denominator_stack=[
            Conv(
                filters=filters,
                kernel_size=1,
                act=conv_act,
                norm=conv_norm,
                name=layer_name(f'{self.block_name}_d',index=i),
                **conv_config)
            for i in range(depth)]
        self.order=order
        self.norm=self._norm(norm,norm_config)
        self.act=self._activation(act,act_config)


    def __call__(self,x):
        numerator=x
        for l in self.numerator_stack:
            numerator=l(numerator)
        denominator=x
        for l in self.denominator_stack:
            denominator=l(denominator)
        x=numerator/(denominator+EPS)
        for m in self.order:
            l=getattr(self,m)
            if l: x=l(x)
        return x


    def _norm(self,norm,norm_config):
        if norm==True:
            norm=Conv.DEFAULT_NORM
        if norm==Conv.BATCH_NORM:
            norm=layers.BatchNormalization(
                name=layer_name(f'{self.block_name}_bn'),
                **norm_config)
        elif norm==Conv.GROUP_NORM:
            norm=addons.GroupNormalization(
                name=layer_name(f'{self.block_name}_gn'),
                **norm_config)
        elif norm:
            raise ValueError('only `group` and `batch` norms implemented')
        else:
            norm=False
        return norm      


    def _activation(self,act,config):
        if act:
            act=get_activation(act,name=layer_name(f'{self.block_name}_act'),**config)
        return act



class Stack(keras.Model):
    """ (Res)Stack of Conv Blocks
    """
    #
    # CONSTANTS
    #
    IDENTITY='ident'



    #
    # PUBLIC
    #
    def __init__(self,
            filters=None,
            kernel_size=3,
            depth=1,
            filters_in=None,
            filters_out=None,
            filters_list=None,
            kernel_size_list=None,
            padding='same',
            squeeze_excitation=False,
            squeeze_excitation_ratio=16,
            channel_squeeze_excitation=False,
            block_squeeze_excitation=False,
            block_squeeze_excitation_config={},
            residual=True,
            residual_act=True,
            residual_norm=None,
            residual_norm_config=None,
            seperable_residual=False,
            seperable=False,
            pointwise_first=False,
            depthwise_out=False,
            norm=True,
            norm_config={},
            output_dropout=True,
            act=True,
            act_config={},
            input_dilation_rate=1,
            output_dilation_rate=1,
            output_stride=1,
            dilation_rate=1,
            max_pooling=False,
            is_skip=False,
            name=None,
            named_layers=True,
            layers_name='conv',
            **conv_config):
        super(Stack, self).__init__()
        self.block_name=name or self.name
        self.named_layers=named_layers
        self.layers_name=layers_name
        if filters_list:
            depth=len(filters_list)
        elif kernel_size_list:
            depth=len(kernel_size_list)
        self.filters_list=self._filters_list(
            filters_list,
            filters,
            filters_in,
            filters_out,
            depth)
        self.kernel_size_list=self._kernel_size_list(
            kernel_size_list,
            kernel_size,
            depth)
        self._set_config(
            act,
            output_stride,
            output_dropout,
            dilation_rate,
            max_pooling,
            seperable=seperable,
            seperable_residual=seperable_residual,
            depthwise_out=depthwise_out,
            pointwise_first=pointwise_first,
            norm=norm,
            norm_config=norm_config,
            padding=padding,
            act_config=act_config,
            **conv_config)
        if squeeze_excitation:
            self.se=SqueezeExcitation(
                filters,
                ratio=squeeze_excitation_ratio)
        elif channel_squeeze_excitation:
            self.se=ChannelSqueezeExcitation(filters)
        elif block_squeeze_excitation:
            self.se=BlockSqueezeExcitation(filters,**block_squeeze_excitation_config)
        else:
            self.se=False
        self.residual=self._residual(
            residual,
            residual_act,
            residual_norm,
            residual_norm_config,
            self.filters_list[-1],
            output_stride)
        if self.residual and padding=='valid':
            self.res_crop=int(kernel_size//2)*len(self.filters_list)
            if (kernel_size/2)==self.res_crop:
                raise ValueError('Residuals with valid padding must have odd kernel_size')
        else:
            self.res_crop=False
        self.stack=self._build_stack(
            output_stride,
            input_dilation_rate,
            output_dilation_rate)
        self.is_skip=is_skip


    def __call__(self,x,training=False,**kwargs):
        if self.residual:
            res=x
            if self.residual!=Stack.IDENTITY:
                if self.res_crop:
                    res=res[:,self.res_crop:-self.res_crop,self.res_crop:-self.res_crop,:]
                res=self.residual(res)
        for layer in self.stack:
            x=layer(x)
        if self.se:
            x=self.se(x)
        if self.residual:
            x=layers.add([res,x])
        return x



    #
    # INTERNAL
    #
    def _filters_list(
            self,
            filters_list,
            filters,
            filters_in,
            filters_out,
            depth):
        if not filters_list:
            if depth==1:
                filters_list=[filters]
            else:
                if filters_in is None:
                    filters_in=filters            
                if filters_out is None:
                    filters_out=filters
                filters_list=[filters_in]+([filters]*(depth-2))+[filters_out]
        return filters_list


    def _kernel_size_list(self,kernel_size_list,kernel_size,depth):
        if not kernel_size_list:
            kernel_size_list=[kernel_size]*depth
        return kernel_size_list


    def _set_config(self,
            act,
            output_stride,
            output_dropout,
            dilation_rate,
            max_pooling,
            seperable,
            seperable_residual,
            depthwise_out,
            norm,
            norm_config,
            **shared_config):
        self.act=act
        self.output_dropout=output_dropout
        self.max_pooling_config=self._max_pooling_config(
            output_stride,
            dilation_rate,
            max_pooling)
        self.seperable=seperable
        self.seperable_residual=seperable_residual
        self.depthwise_out=depthwise_out
        self.norm=norm
        self.norm_config=norm_config
        shared_config['dilation_rate']=dilation_rate
        self.shared_config=shared_config


    def _max_pooling_config(self,output_stride,dilation_rate,max_pooling):
        if max_pooling and (output_stride==2) and (dilation_rate==1):
            if max_pooling is True:
                max_pooling=DEFAULT_MAX_POOLING
            return max_pooling
        else:
            return False


    def _layer_name(self,name,index=None):
        return layer_name(self.block_name,name,index=index,named=self.named_layers)


    def _residual(
            self,
            residual,
            residual_act,
            residual_norm,
            residual_norm_config,
            filters,
            output_stride):
        if residual and (residual!=Stack.IDENTITY):
            if not residual_act:
                act=False
            else:
                act=self.act
            if residual_norm is None:
                residual_norm=self.norm
            if residual_norm_config is None:
                residual_norm_config=self.norm_config
            cfig=self.shared_config.copy()
            cfig['dropout']=False
            residual=Conv(
                filters=filters,
                kernel_size=1,
                strides=output_stride,
                seperable=self.seperable_residual,
                act=act,
                name=self._layer_name('residual'),
                named_layers=self.named_layers,
                norm=residual_norm,
                norm_config=residual_norm_config,
                **cfig)
        return residual

    
    def _build_stack(self,
            output_stride,
            input_dilation_rate,
            output_dilation_rate):
        _layers=[] 
        last_layer_index=len(self.filters_list)-1
        for i,(f,k) in enumerate(zip(self.filters_list,self.kernel_size_list)):
            cfig=self.shared_config.copy()
            strides=cfig.pop('strides',1)
            dilation_rate=cfig.pop('dilation_rate',1)
            if (i==0):
                dilation_rate=input_dilation_rate or dilation_rate
                seperable=self.seperable
                depthwise=False
            elif self.depthwise_out:
                seperable=False
                depthwise=True
            if (i==last_layer_index):
                if not self.output_dropout:
                    cfig['dropout']=False
                if (not self.max_pooling_config):
                    strides=output_stride or strides
                    dilation_rate=output_dilation_rate or dilation_rate
            _layers.append(Conv(
                filters=f,
                kernel_size=k,
                strides=strides,
                dilation_rate=dilation_rate,
                seperable=seperable,
                depthwise=depthwise,
                act=self.act,
                norm=self.norm,
                norm_config=self.norm_config,
                name=self._layer_name(self.layers_name,index=i),
                named_layers=self.named_layers,
                **cfig))
            if (i==last_layer_index) and self.max_pooling_config:
                _layers.append(layers.MaxPooling2D(
                    **self.max_pooling_config))
        return _layers


class Parallel(keras.Model):
    """ Parallel Configs
    """
    #
    # CONSTANTS
    #
    MERGE_TYPE='add'
    MERGE_TYPES=['add','average']


    #
    # PUBLIC
    #
    def __init__(self,
            blocks_configs,
            merge_type=MERGE_TYPE):
        super(Parallel, self).__init__()
        self.stacks=[]
        for bcfig in blocks_configs:
            if isinstance(bcfig,dict):
                bcfig=bcfig.pop('blocks_config',bcfig)
            stacked_blocks=[build_blocks(c) for c in bcfig]
            self.stacks.append(stacked_blocks)
        self.merge_type=merge_type
        if self.merge_type not in Parallel.MERGE_TYPES:
            print (
                '[WARNING] tfbox.nn.blocks.Parallel: using non-standard merge',
                self.merge_type
            )

    def __call__(self,x,training=False,**kwargs):
        outs=[]
        for stacked_blocks in self.stacks:
            outs.append(self._call_stack(stacked_blocks,x))
        return self._merge(outs)

    def _call_stack(self,stacked_blocks,x):
        for sb in stacked_blocks:
            for block in sb:
                x=block(x)
        return x

    def _merge(self,outputs):
        if len(outputs)>1:
            return getattr(layers,self.merge_type)(outputs)
        else:
            return outputs[0]




class Group(keras.Model):
    """ (Res)Parallel Group of Conv Blocks
    """
    #
    # CONSTANTS
    #
    IDENTITY='ident'



    #
    # PUBLIC
    #
    def __init__(self,
            filters,
            hidden_filters=None,
            kernel_size_list=[1,3,3],
            kernel_size_out=1,
            dilation_rate_list=[1,6,12],
            global_pooling=False,
            residual=True,
            residual_act=True,
            seperable=False,
            act=True,
            act_config={},
            act_last=False,
            padding='same',
            out_config={},
            is_skip=False,
            name=None,
            named_layers=True,
            layers_name='conv',
            **conv_config):
        super(Group, self).__init__()
        if padding is not 'same':
            raise NotImplementedError('currently only accepts padding=same')
        self.block_name=name or self.name
        self.named_layers=named_layers
        self.layers_name=layers_name
        self._set_config(
                kernel_size_list,
                dilation_rate_list,
                filters,
                hidden_filters,
                act,
                act_config,
                padding=padding,
                **conv_config)
        self.residual=self._residual(residual,residual_act)
        self.pooling_stack=self._global_pooling(global_pooling)
        self.group=self._build_group()
        self.out_conv=self._out_conv(kernel_size_out,out_config)
        self.is_skip=is_skip


    def __call__(self,x,training=False,**kwargs):
        if self.residual==Group.IDENTITY:
            res=x
        elif self.residual:
            res=self.residual(x)
        else:
            res=False
        x=self._call_group(x)
        if self.out_conv:
            x=self.out_conv(x)
        if res is not False:
            x=layers.add([res,x])
        return x



    #
    # INTERNAL
    #
    def _layer_name(self,name,index=None):
        return layer_name(self.block_name,name,index=index,named=self.named_layers)


    def _call_group(self,x):
        _x=[]
        for layer in self.group:
            _x.append(layer(x))
        if self.pooling_stack:
            shape=x.shape
            for layer in self.pooling_stack:
                x=layer(x)
            x=upsample(x,shape=shape)
            _x.append(x)
        return layers.Concatenate()(_x) 


    def _set_config(self,
            kernel_size_list,
            dilation_rate_list,
            filters,
            hidden_filters,
            act,
            act_config,
            **shared_config):
        self.kernel_size_list=kernel_size_list
        self.dilation_rate_list=dilation_rate_list
        self.filters=filters
        if not hidden_filters:
            hidden_filters=filters
        self.hidden_filters=hidden_filters
        self.act=act
        self.act_config=act_config
        self.shared_config=shared_config


    def _global_pooling(self,global_pooling):
        if not global_pooling:
            return False
        else:
            if global_pooling is True:
                global_pooling=DEFAULT_GLOBAL_POOLING
            _layers=[]
            if global_pooling in ['max','gmp','global_max_pooling']:
                _layers.append(layers.GlobalMaxPooling2D())
            else:
                _layers.append(layers.GlobalAveragePooling2D())
            _layers.append(layers.Lambda(
                lambda x:  tf.expand_dims(tf.expand_dims(x, axis=1),axis=1)
            ))
            _layers.append(layers.Conv2D(
                filters=self.hidden_filters,
                kernel_size=1, 
                strides=1,
                use_bias=False,
                name=self._layer_name('global_pooling'),
            ))
            return _layers


    def _residual(self,residual,residual_act):
        if residual and (residual!=Stack.IDENTITY):
            if not residual_act:
                act=False
            else:
                act=self.act
            residual=Conv(
                filters=self.hidden_filters,
                kernel_size=1,
                act=act,
                act_config=self.act_config,
                name=self._layer_name('residual',index=i),
                named_layers=self.named_layers,
                **self.shared_config)
        return residual

    
    def _build_group(self):
        _layers=[] 
        for i,(k,d) in enumerate(zip(self.kernel_size_list,self.dilation_rate_list)):
            _layers.append(Conv(
                filters=self.hidden_filters,
                kernel_size=k,
                dilation_rate=d,
                act=self.act,
                act_config=self.act_config,
                name=self._layer_name(self.layers_name,index=i),
                named_layers=self.named_layers,
                **self.shared_config))
        return _layers       


    def _out_conv(self,kernel_size,out_config):
        if self.filters:
            config=self.shared_config.copy()
            config['act']=self.act
            config['act_config']=self.act_config
            config.update(out_config)
            return Conv(
                filters=self.filters,
                kernel_size=kernel_size,
                name=self._layer_name('out_conv'),
                named_layers=self.named_layers,
                **config)




#
# BLOCKS 
#
class SqueezeExcitation(keras.Model):
    """ SqueezeExcitation
    """


    def __init__(self,filters,ratio=16,global_pooling='avg'):
        super(SqueezeExcitation, self).__init__()
        if global_pooling in ['max','gmp','global_max_pooling']:
            self.gp=layers.GlobalMaxPooling2D()
        else:
            self.gp=layers.GlobalAveragePooling2D()
        self.reduce=layers.Dense(filters//ratio,activation='relu')
        self.expand=layers.Dense(filters,activation='sigmoid')


    def __call__(self,x,training=False):
        y=self.gp(x)
        y=self.reduce(y)
        y=self.expand(y)
        return layers.multiply([x,y])


class BlockSqueezeExcitation(keras.Model):
    """ BlockSqueezeExcitation
    """

    def __init__(self,
            filters,
            ratio=16,
            pool_type='avg',
            pool_size=None,
            size=None,
            grid_size=3):
        super(BlockSqueezeExcitation, self).__init__()
        if pool_type in ['avg','max']:
            self.pool_type=pool_type
        else:
            raise ValueError('BlockSqueezeExcitation: pooling must be max or avg')
        self.pooling=None
        self.reduce=layers.Dense(filters//ratio,activation='relu')
        self.expand=layers.Dense(filters,activation='sigmoid')
        self.up=None
        self.grid_size=grid_size
        self.pool_size=pool_size
        self._set_pool_up(size)


    def _get_pool_layer(self):
        if self.pool_type=='avg':
            return layers.AveragePooling2D
        elif self.pool_type=='max':
            return layers.MaxPool2D
 

    def _set_pool_up(self,size):
        if self.pool_size:
            self.pooling=self._get_pool_layer()(self.pool_size,padding='same',strides=1)
            self.up=False
        elif size:
            _ps=size/self.grid_size
            self.pool_size=int(_ps)
            if _ps!=self.pool_size:
                raise ValueError('BlockSqueezeExcitation: grid_size/size must an integer') 
            self.pooling=self._get_pool_layer()(self.pool_size,padding='same')
            self.up=layers.UpSampling2D(self.pool_size)


    def __call__(self,x,training=False):
        if not self.pooling:
            self._set_pool_up(x.shape[1])  
        y=self.pooling(x)
        y=self.reduce(y)
        y=self.expand(y)
        if self.up:
            y=self.up(y)
        return layers.multiply([x,y])


class ChannelSqueezeExcitation(keras.Model):
    """ ChannelSqueezeExcitation
    """

    def __init__(self,filters,**squeeze_kwargs):
        super(ChannelSqueezeExcitation, self).__init__()
        self.squeeze=layers.Conv2D(1,1,activation='sigmoid',**squeeze_kwargs)


    def __call__(self,x):
        y=self.squeeze(x)
        return layers.multiply([x,y])




class Residual(keras.Model):
    """ Residual
    """
    IDENTITY='identity'


    def __init__(self,
            block,
            identity=False,
            filters=None,
            residual=True,
            concat=False,
            **config):
        super(Residual, self).__init__()
        if isinstance(block,dict):
            self.block=build_blocks(block)
        else:
            self.block=block
        self.concat=concat
        self.residual=self._residual(
            residual,
            identity,
            filters,
            config)


    def __call__(self,x,training=False):
        if self.residual==Residual.IDENTITY:
            res=x
        elif self.residual:
            res=self.residual(x)
        else:
            res=False
        if isinstance(self.block,list):
            for b in self.block:
                x=b(x)        
        else:
            x=self.block(x)
        if res is not False:
            if self.concat:
                x=layers.Concatenate()([res,x])
            else:
                x=layers.add([res,x])
        return x


    #
    # INTERNAL
    #
    def _residual(self,residual,identity,filters,config):
        if residual:
            if identity:
                residual=Residual.IDENTITY
            else:
                residual=Conv(
                    filters=filters,
                    kernel_size=1,
                    **config)
        return residual



#
# PRE-CONFIGURED BLOCKS
#
class ASPP(Group):
    """ ASPP (convenience wrapper for Group)
    """
    #
    # CONSTANTS
    #
    IDENTITY='ident'



    #
    # PUBLIC
    #
    def __init__(self,
            config='aspp',
            file_name='blocks',
            folder=load.TFBOX,
            **kwargs):
        config=load.config(config=config,file_name=file_name,folder=folder)
        config.update(kwargs)
        super(ASPP, self).__init__(**config)




def get_fixed_initializer(value):
    """
    Args: 
        * value(tensor): a tensor to use for initialization
    """
    def _fixed_initializer(shape,dtype=None):
        if shape[-1]!=len(value):
            raise ValueError('Fixed Initializer: input must match shape',len(value),shape)
        return value
    return _fixed_initializer


class SegmentClassifier(keras.Model):
    """
    """
    #
    # CONSTANTS
    #
    AUTO='auto'


    #
    # PUBLIC
    #
    def __init__(self,
            nb_classes,
            depth=1,
            filters=None,
            filters_list=None,
            kernel_size=3,
            kernel_size_list=None,
            output_norm=True,
            output_norm_config={},
            output_act=True,
            output_act_config={},
            seperable_preclassification=False,
            residual_preclassification=False,
            bias_class_weights=None,
            name=None,
            named_layers=True,
            padding='same',
            **stack_config):
        super(SegmentClassifier, self).__init__()
        self.block_name=name or self.name
        self.named_layers=named_layers
        kernel_size_list=self._kernel_size_list(
            kernel_size_list,
            kernel_size,
            depth)
        filters_list=self._filters_list(
            filters_list,
            filters,
            nb_classes,
            len(kernel_size_list))
        if filters_list and len(filters_list)>1:
            self.preclassifier=Stack(
                filters_list=filters_list[:-1],
                kernel_size_list=kernel_size_list[:-1],
                padding=padding,
                seperable=seperable_preclassification,
                residual=residual_preclassification,
                name=self._layer_name('stack'),
                named_layers=self.named_layers,
                **stack_config)
        else:
            self.preclassifier=False
        if filters_list:
            if bias_class_weights:
                _=bias_class_weights
                bias_class_weights=tf.convert_to_tensor(
                    bias_class_weights,
                    dtype=tf.dtypes.float32)
                bias_class_weights=bias_class_weights/tf.reduce_sum(bias_class_weights)
                bias_class_weights=tf.math.log(bias_class_weights+EPS)
                print('FIXED BIAS INITIALIZER:',_,tf.nn.softmax(bias_class_weights))
                bias_initializer=get_fixed_initializer(bias_class_weights)
            else:
                bias_initializer='zeros'
            self.classifier=Conv(
                    filters=filters_list[-1],
                    kernel_size=kernel_size_list[-1],
                    padding=padding,
                    norm=output_norm,
                    norm_config=output_norm_config,
                    act=False,
                    bias_initializer=bias_initializer,
                    name=self.block_name,
                    named_layers=self.named_layers)
        else:
            self.classifier=False
        self.act=self._activation(nb_classes,output_act,output_act_config)



    def __call__(self,x,training=False,**kwargs):
        if self.preclassifier:
            x=self.preclassifier(x)
        if self.classifier:
            x=self.classifier(x)
        if self.act:
            x=self.act(x)
        return x



    #
    # INTERNAL
    #
    def _layer_name(self,name,index=None):
        return layer_name(self.block_name,name,index=index,named=self.named_layers)


    def _filters_list(self,filters_list,filters,nb_classes,depth):
        if filters_list:
            out_filters=filters_list[-1]
            if h.noney(out_filters):
                filters_list[-1]=nb_classes
            elif filters_list[-1]!=nb_classes:
                raise ValueError('last filters value must equal nb_classes')
        else:
            if filters is False:
                filters_list=None
            else:
                if filters is None:
                    filters=nb_classes
                filters_list=[filters]*(depth-1)+[nb_classes]
        return filters_list


    def _kernel_size_list(self,kernel_size_list,kernel_size,depth):
        if not kernel_size_list:
            kernel_size_list=[kernel_size]*depth
        return kernel_size_list


    def _activation(self,nb_classes,act,config):
        if (act is True) or (act==SegmentClassifier.AUTO):
            if nb_classes==1:
                act='sigmoid'
            else:
                act='softmax'
        print('OUTPUT_ACTIVATION:',act,config)
        if act:
            act=get_activation(act,name=self._layer_name('activation'),**config)
        return act


#
# TBOX DICTS
#
BLOCKS={
    'conv': Conv,
    'stack': Stack,
    'group': Group,
    'parallel': Parallel,
    'groups': addons.Groups,
    'residual': Residual,
    'squeeze_excitation': SqueezeExcitation,
    'aspp': ASPP,
    'band_math': BandMath,
    'segment_classifier': SegmentClassifier
}
ACTIVATIONS={
    'relu': layers.ReLU,
    'sigmoid': activations.sigmoid,
    'swish': addons.Swish,
    'softmax': layers.Softmax
}
STACK_BTYPE='stack'
CONV_BTYPE='conv'
INT_BTYPE=CONV_BTYPE
DEFAULT_BTYPE=STACK_BTYPE



