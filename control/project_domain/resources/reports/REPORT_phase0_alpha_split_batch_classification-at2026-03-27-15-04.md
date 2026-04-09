# Phase0 Alpha Split Batch Classification Report

## Purpose

Classify which PPT-extracted images are already good enough for deterministic alpha split without ImageSorcery fallback.

## Batch Surface

- input_root: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs`
- worker_script: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py`
- worker_python: `/opt/homebrew/Cellar/python@3.13/3.13.6/Frameworks/Python.framework/Versions/3.13/bin/python3.13`
- alpha_threshold: `1`
- min_pixels: `32`
- padding: `4`
- min_components_for_success: `2`

## Summary

- total_images: `61`
- unsupported_source_format: `1`
- worker_error: `60`

## Alpha-Split-Sufficient Candidates

- none

## Single-Component-Only Cases

- none

## Non-Alpha Or Opaque-Surface Cases

- none

## No-Component Cases

- none

## Worker Errors

- `01_full_presentation_2026-03-17:image1.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image10.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image11.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image12.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image13.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image14.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image15.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image2.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image3.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image4.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image5.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image7.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image8.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `01_full_presentation_2026-03-17:image9.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image1.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image10.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image11.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image12.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image13.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image14.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image15.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image16.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image17.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image18.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image19.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image2.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image20.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image21.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image22.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image23.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image24.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image25.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image26.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image27.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image28.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image29.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image3.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image30.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image31.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image32.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image33.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image34.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image35.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image36.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image37.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image38.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image39.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image4.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image40.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image41.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image42.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image43.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image44.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image45.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image46.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image5.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image6.jpeg` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image7.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image8.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
- `02_1:image9.png` error: Traceback (most recent call last):
  File "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py", line 13, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'

## Recommendation

- only the `alpha_split_sufficient` subset should move forward as deterministic split candidates
- keep all other images on the full-image + standalone OCR baseline
- do not turn on automatic object-isolation batch fanout for the insufficient subset yet
