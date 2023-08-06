from brevettiai.model.factory.mobilenetv2_backbone import lightning_segmentation_backbone, \
    thunder_segmentation_backbone, MobileNetV2SegmentationBackbone
from brevettiai.model.factory.lenet_backbone import lenet_backbone
from brevettiai.model.factory.lraspp import LRASPP2SegmentationHead, LRASPPSegmentationHead
from brevettiai.model.factory.unet import UnetSegmentationHead
# from brevettiai.model.factory.segmentation import SegmentationModelFactory
from brevettiai.model.metadata.image_segmentation import ImageSegmentationModelMetadata
from functools import partial


extended_backbone = partial(
    MobileNetV2SegmentationBackbone,
    output_layers=['block_1_expand_relu', 'block_6_expand_relu', 'block_13_expand_relu'],
    alpha=1
)

backbones = {
    "lightning": lightning_segmentation_backbone,
    "thunder": thunder_segmentation_backbone,
    "extended": extended_backbone,
    "lenet": lenet_backbone

}

heads = {
    "lraspp": LRASPPSegmentationHead,
    "lraspp2": LRASPP2SegmentationHead,
    "unet": UnetSegmentationHead
}

catalogue={"backbones": backbones, "heads": heads}