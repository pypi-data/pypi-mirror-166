from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class FilterFramesByLabelISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the filter-frames-od ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Filters frames from the stream using the labels in the annotations, i.e., keeps or drops frames depending on presence/absence of labels."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        from wai.annotations.domain.image.segmentation import ImageSegmentationDomainSpecifier
        if input_domain is ImageClassificationDomainSpecifier:
            return input_domain
        elif input_domain is ImageObjectDetectionDomainSpecifier:
            return input_domain
        elif input_domain is ImageSegmentationDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"FilterFrames only handles the following domains: "
                f"{ImageObjectDetectionDomainSpecifier.name()}, "
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.video.isp.filter_frames_by_label.component import FilterFramesByLabel
        return FilterFramesByLabel,
