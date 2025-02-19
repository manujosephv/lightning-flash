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

import numpy as np
import pytest

from flash.core.data.utilities.loading import (
    AUDIO_EXTENSIONS,
    CSV_EXTENSIONS,
    IMG_EXTENSIONS,
    NP_EXTENSIONS,
    TSV_EXTENSIONS,
    load_audio,
    load_data_frame,
    load_image,
    load_spectrogram,
)
from flash.core.utilities.imports import (
    _PANDAS_AVAILABLE,
    _TOPIC_AUDIO_AVAILABLE,
    _TOPIC_IMAGE_AVAILABLE,
    _TOPIC_TABULAR_AVAILABLE,
    Image,
)

if _TOPIC_AUDIO_AVAILABLE:
    import soundfile as sf

if _PANDAS_AVAILABLE:
    from pandas import DataFrame
else:
    DataFrame = object


def write_image(file_path):
    Image.fromarray(np.random.randint(0, 255, (64, 64, 3), dtype="uint8")).save(file_path)


def write_numpy(file_path):
    np.save(file_path, np.random.randint(0, 255, (64, 64, 3), dtype="uint8"))


def write_audio(file_path):
    samplerate = 1000
    data = np.random.uniform(-1, 1, size=(samplerate, 2))
    subtype = "VORBIS" if "ogg" in file_path else "PCM_16"
    format = "mat5" if "mat" in file_path else None
    sf.write(file_path, data, samplerate, subtype=subtype, format=format)


def write_csv(file_path):
    DataFrame.from_dict(
        {
            "animal": ["cat", "dog", "cat"],
            "friendly": ["yes", "yes", "no"],
            "weight": [6, 10, 5],
        }
    ).to_csv(file_path)


def write_tsv(file_path):
    DataFrame.from_dict(
        {
            "animal": ["cat", "dog", "cat"],
            "friendly": ["yes", "yes", "no"],
            "weight": [6, 10, 5],
        }
    ).to_csv(file_path, sep="\t")


@pytest.mark.skipif(not _TOPIC_IMAGE_AVAILABLE, reason="image libraries aren't installed.")
@pytest.mark.parametrize(
    ("extension", "write"),
    [(extension, write_image) for extension in IMG_EXTENSIONS]
    + [(extension, write_numpy) for extension in NP_EXTENSIONS]
    # it shouldn't try to expand glob patterns in filenames
    + [(filename, write_image) for filename in ("image [test].jpeg",)],
)
def test_load_image(tmpdir, extension, write):
    file_path = os.path.join(tmpdir, f"test{extension}")
    write(file_path)

    image = load_image(file_path)

    assert isinstance(image, Image.Image)
    assert image.mode == "RGB"


@pytest.mark.skipif(not _TOPIC_AUDIO_AVAILABLE, reason="audio libraries aren't installed.")
@pytest.mark.parametrize(
    ("extension", "write"),
    [(extension, write_image) for extension in IMG_EXTENSIONS]
    + [(extension, write_numpy) for extension in NP_EXTENSIONS]
    + [(extension, write_audio) for extension in AUDIO_EXTENSIONS],
)
def test_load_spectrogram(tmpdir, extension, write):
    file_path = os.path.join(tmpdir, f"test{extension}")
    write(file_path)

    spectrogram = load_spectrogram(file_path)

    assert isinstance(spectrogram, np.ndarray)
    assert spectrogram.dtype == np.dtype("float32")


@pytest.mark.skipif(not _TOPIC_AUDIO_AVAILABLE, reason="audio libraries aren't installed.")
@pytest.mark.parametrize(("extension", "write"), [(extension, write_audio) for extension in AUDIO_EXTENSIONS])
def test_load_audio(tmpdir, extension, write):
    file_path = os.path.join(tmpdir, f"test{extension}")
    write(file_path)

    audio = load_audio(file_path)

    assert isinstance(audio, np.ndarray)
    assert audio.dtype == np.dtype("float32")


@pytest.mark.skipif(not _TOPIC_TABULAR_AVAILABLE, reason="tabular libraries aren't installed.")
@pytest.mark.parametrize(
    ("extension", "write"),
    [(extension, write_csv) for extension in CSV_EXTENSIONS] + [(extension, write_tsv) for extension in TSV_EXTENSIONS],
)
def test_load_data_frame(tmpdir, extension, write):
    file_path = os.path.join(tmpdir, f"test{extension}")
    write(file_path)

    data_frame = load_data_frame(file_path)

    assert isinstance(data_frame, DataFrame)


@pytest.mark.parametrize(
    ("path", "loader", "target_type"),
    [
        pytest.param(
            "https://pl-flash-data.s3.amazonaws.com/images/ant_1.jpg",
            load_image,
            Image.Image,
            marks=pytest.mark.skipif(not _TOPIC_IMAGE_AVAILABLE, reason="image libraries aren't installed."),
        ),
        # it shouldn't try to expand glob patterns in URLs
        pytest.param(
            "https://pl-flash-data.s3.amazonaws.com/images/ant_1 [test].jpg",
            load_image,
            Image.Image,
            marks=pytest.mark.skipif(not _TOPIC_IMAGE_AVAILABLE, reason="image libraries aren't installed."),
        ),
        pytest.param(
            "https://pl-flash-data.s3.amazonaws.com/images/ant_1.jpg",
            load_spectrogram,
            np.ndarray,
            marks=pytest.mark.skipif(not _TOPIC_AUDIO_AVAILABLE, reason="audio libraries aren't installed."),
        ),
        pytest.param(
            "https://pl-flash-data.s3.amazonaws.com/titanic.csv",
            load_data_frame,
            DataFrame,
            marks=pytest.mark.skipif(not _TOPIC_TABULAR_AVAILABLE, reason="tabular libraries aren't installed."),
        ),
    ],
)
def test_load_remote(path, loader, target_type):
    assert isinstance(loader(path), target_type)
