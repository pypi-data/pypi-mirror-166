from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image import ImageInstance


class FilterFramesByLabel(
    RequiresNoFinalisation,
    ProcessorComponent[ImageInstance, ImageInstance]
):
    """
    Stream processor which filters frames based on labels and scores.
    """

    verbose: str = FlagOption(
        "-v", "--verbose",
        help="whether to output debugging information."
    )

    key_label: str = TypedOption(
        "--key-label",
        type=str,
        default="type",
        help="the meta-data key in the annotations that contains the label."
    )

    required_labels: str = TypedOption(
        "--required-labels",
        type=str,
        default="",
        help="the comma-separated list of labels that must be present in the frame, otherwise it gets dropped"
    )

    excluded_labels: str = TypedOption(
        "--excluded-labels",
        type=str,
        default="",
        help="the comma-separated list of labels that will automatically drop the frame when present in the frame"
    )

    key_score: str = TypedOption(
        "--key-score",
        type=str,
        default="score",
        help="the meta-data key in the annotations to use for storing the prediction score."
    )

    min_score: float = TypedOption(
        "--min-score",
        type=float,
        help="the minimum score that predictions must have in order to be included in the label checks, ignored if not supplied"
    )

    def _initialize(self):
        """
        Initializes the labels, etc.
        """
        if len(self.required_labels) > 0:
            self._required_labels = set(self.required_labels.split(","))
        else:
            self._required_labels = None
        if len(self.excluded_labels) > 0:
            self._excluded_labels = set(self.excluded_labels.split(","))
        else:
            self._excluded_labels = None

    def process_element(
            self,
            element: ImageInstance,
            then: ThenFunction[ImageInstance],
            done: DoneFunction
    ):
        if not hasattr(self, "_required_labels"):
            self._initialize()

        ignored = set()

        # min score
        if (self.min_score is not None) and (self.min_score > 0):
            for index, obj in enumerate(element.annotations):
                if self.key_score in obj.metadata:
                    if float(obj.metadata[self.key_score]) < self.min_score:
                        ignored.add(index)
                else:
                    ignored.add(index)

            # remove objects
            if len(ignored) > 0:
                if self.verbose:
                    self.logger.info("Ignoring %d annotation(s) due to min_score of %f" % (len(ignored), self.min_score))

        # check labels
        keep = False
        skip = False

        # 1. required labels
        if self._required_labels is not None:
            for index, obj in enumerate(element.annotations):
                if index in ignored:
                    continue
                if self.key_label in obj.metadata:
                    if str(obj.metadata[self.key_label]) in self._required_labels:
                        keep = True
                else:
                    skip = True

        # 2. excluded labels
        if self._excluded_labels is not None:
            for index, obj in enumerate(element.annotations):
                if index in ignored:
                    continue
                if self.key_label in obj.metadata:
                    if str(obj.metadata[self.key_label]) in self._excluded_labels:
                        skip = True
                else:
                    skip = True

        # drop frame?
        if skip or not keep:
            return

        then(element)
