# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import torch

from flash.core.utilities.imports import (
    _BAAL_AVAILABLE,
    _FIFTYONE_AVAILABLE,
    _ICEDATA_AVAILABLE,
    _ICEVISION_AVAILABLE,
    _LEARN2LEARN_AVAILABLE,
    _SEGMENTATION_MODELS_AVAILABLE,
    _TOPIC_AUDIO_AVAILABLE,
    _TOPIC_CORE_AVAILABLE,
    _TOPIC_GRAPH_AVAILABLE,
    _TOPIC_IMAGE_AVAILABLE,
    _TOPIC_POINTCLOUD_AVAILABLE,
    _TOPIC_TABULAR_AVAILABLE,
    _TOPIC_TEXT_AVAILABLE,
    _TOPIC_VIDEO_AVAILABLE,
    _TORCHVISION_GREATER_EQUAL_0_9,
    _VISSL_AVAILABLE,
)
from tests.examples.helpers import run_test
from tests.helpers.decorators import forked

root = Path(__file__).parent.parent.parent


@patch.dict(os.environ, {"FLASH_TESTING": "1"})
@pytest.mark.parametrize(
    ("folder", "fname"),
    [
        pytest.param(
            "",
            "template.py",
            marks=[
                pytest.mark.skipif(not _TOPIC_CORE_AVAILABLE, reason="Not testing core."),
                pytest.mark.skipif(os.name == "posix", reason="Flaky on Mac OS (CI)"),
                pytest.mark.skipif(sys.version_info >= (3, 9), reason="Undiagnosed segmentation fault in 3.9"),
            ],
        ),
        pytest.param(
            "audio",
            "audio_classification.py",
            marks=pytest.mark.skipif(not _TOPIC_AUDIO_AVAILABLE, reason="audio libraries aren't installed"),
        ),
        pytest.param(
            "audio",
            "speech_recognition.py",
            marks=pytest.mark.skipif(not _TOPIC_AUDIO_AVAILABLE, reason="audio libraries aren't installed"),
        ),
        pytest.param(
            "image",
            "image_classification.py",
            marks=pytest.mark.skipif(not _TOPIC_IMAGE_AVAILABLE, reason="image libraries aren't installed"),
        ),
        pytest.param(
            "image",
            "image_classification_multi_label.py",
            marks=pytest.mark.skipif(not _TOPIC_IMAGE_AVAILABLE, reason="image libraries aren't installed"),
        ),
        pytest.param(
            "image",
            "image_embedder.py",
            marks=[
                pytest.mark.skipif(not _TOPIC_IMAGE_AVAILABLE, reason="image libraries aren't installed"),
                pytest.mark.skipif(not _VISSL_AVAILABLE, reason="VISSL package isn't installed"),
                pytest.mark.skipif(torch.cuda.device_count() > 1, reason="VISSL integration doesn't support multi-GPU"),
            ],
        ),
        pytest.param(
            "image",
            "object_detection.py",
            marks=pytest.mark.skipif(
                not (_TOPIC_IMAGE_AVAILABLE and _ICEVISION_AVAILABLE), reason="image libraries aren't installed"
            ),
        ),
        pytest.param(
            "image",
            "instance_segmentation.py",
            marks=[
                pytest.mark.skipif(not _TOPIC_IMAGE_AVAILABLE, reason="image libraries aren't installed"),
                pytest.mark.skipif(not _ICEDATA_AVAILABLE, reason="icedata package isn't installed"),
                pytest.mark.xfail(strict=False),  # ToDo
            ],
        ),
        pytest.param(
            "image",
            "keypoint_detection.py",
            marks=[
                pytest.mark.skipif(not _TOPIC_IMAGE_AVAILABLE, reason="image libraries aren't installed"),
                pytest.mark.skipif(not _ICEDATA_AVAILABLE, reason="icedata package isn't installed"),
            ],
        ),
        pytest.param(
            "image",
            "semantic_segmentation.py",
            marks=[
                pytest.mark.skipif(not _TOPIC_IMAGE_AVAILABLE, reason="image libraries aren't installed"),
                pytest.mark.skipif(not _SEGMENTATION_MODELS_AVAILABLE, reason="Segmentation package isn't installed"),
                pytest.mark.skipif(not _TORCHVISION_GREATER_EQUAL_0_9, reason="Newer version of TV is needed."),
            ],
        ),
        pytest.param(
            "image",
            "style_transfer.py",
            marks=[
                pytest.mark.skipif(not _TOPIC_IMAGE_AVAILABLE, reason="image libraries aren't installed"),
                pytest.mark.skipif(torch.cuda.device_count() >= 2, reason="PyStiche doesn't support DDP"),
            ],
        ),
        pytest.param(
            "text",
            "question_answering.py",
            marks=pytest.mark.skipif(not _TOPIC_TEXT_AVAILABLE, reason="text libraries aren't installed"),
        ),
        pytest.param(
            "text",
            "summarization.py",
            marks=pytest.mark.skipif(not _TOPIC_TEXT_AVAILABLE, reason="text libraries aren't installed"),
        ),
        pytest.param(
            "tabular",
            "tabular_classification.py",
            marks=pytest.mark.skipif(not _TOPIC_TABULAR_AVAILABLE, reason="tabular libraries aren't installed"),
        ),
        pytest.param(
            "tabular",
            "tabular_regression.py",
            marks=pytest.mark.skipif(not _TOPIC_TABULAR_AVAILABLE, reason="tabular libraries aren't installed"),
        ),
        pytest.param(
            "tabular",
            "tabular_forecasting.py",
            marks=pytest.mark.skipif(not _TOPIC_TABULAR_AVAILABLE, reason="tabular libraries aren't installed"),
        ),
        pytest.param(
            "text",
            "text_classification.py",
            marks=pytest.mark.skipif(not _TOPIC_TEXT_AVAILABLE, reason="text libraries aren't installed"),
        ),
        pytest.param(
            "text",
            "text_embedder.py",
            marks=pytest.mark.skipif(not _TOPIC_TEXT_AVAILABLE, reason="text libraries aren't installed"),
        ),
        # pytest.param(
        #     "text_classification_multi_label.py",
        #     marks=pytest.mark.skipif(not _TOPIC_TEXT_AVAILABLE, reason="text libraries aren't installed")
        # ),
        pytest.param(
            "text",
            "translation.py",
            marks=[
                pytest.mark.skipif(not _TOPIC_TEXT_AVAILABLE, reason="text libraries aren't installed"),
                pytest.mark.skipif(os.name == "nt", reason="Encoding issues on Windows"),
            ],
        ),
        pytest.param(
            "video",
            "video_classification.py",
            marks=pytest.mark.skipif(not _TOPIC_VIDEO_AVAILABLE, reason="video libraries aren't installed"),
        ),
        pytest.param(
            "pointcloud",
            "pcloud_segmentation.py",
            marks=pytest.mark.skipif(not _TOPIC_POINTCLOUD_AVAILABLE, reason="pointcloud libraries aren't installed"),
        ),
        pytest.param(
            "pointcloud",
            "pcloud_detection.py",
            marks=pytest.mark.skipif(not _TOPIC_POINTCLOUD_AVAILABLE, reason="pointcloud libraries aren't installed"),
        ),
        pytest.param(
            "graph",
            "graph_classification.py",
            marks=pytest.mark.skipif(not _TOPIC_GRAPH_AVAILABLE, reason="graph libraries aren't installed"),
        ),
        pytest.param(
            "graph",
            "graph_embedder.py",
            marks=pytest.mark.skipif(not _TOPIC_GRAPH_AVAILABLE, reason="graph libraries aren't installed"),
        ),
        pytest.param(
            "image",
            "fiftyone_img_classification.py",
            marks=pytest.mark.skipif(
                not (_TOPIC_IMAGE_AVAILABLE and _FIFTYONE_AVAILABLE), reason="fiftyone library isn't installed"
            ),
        ),
        pytest.param(
            "image",
            "fiftyone_object_detection.py",
            marks=pytest.mark.skipif(
                not (_TOPIC_IMAGE_AVAILABLE and _FIFTYONE_AVAILABLE), reason="fiftyone library isn't installed"
            ),
        ),
        pytest.param(
            "image",
            "baal_img_classification_active_learning.py",
            marks=pytest.mark.skipif(
                not (_TOPIC_IMAGE_AVAILABLE and _BAAL_AVAILABLE), reason="baal library isn't installed"
            ),
        ),
        pytest.param(
            "image",
            "learn2learn_img_classification_imagenette.py",
            marks=[
                pytest.mark.skip("MiniImagenet broken: https://github.com/learnables/learn2learn/issues/291"),
                pytest.mark.skipif(
                    not (_TOPIC_IMAGE_AVAILABLE and _LEARN2LEARN_AVAILABLE), reason="learn2learn isn't installed"
                ),
            ],
        ),
    ],
)
@forked
@pytest.mark.skipif(sys.platform == "darwin", reason="Fatal Python error: Illegal instruction")  # fixme
def test_example(folder, fname):
    run_test(str(root / "examples" / folder / fname))
