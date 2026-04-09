# ISSUE: Objective-Profile Mismatch Hides True Candidate Winner

## Summary

A regrouped candidate can look promising only because the objective was underspecified. Dashboard-overview scoring and table-focus scoring may choose different winners, and treating them as the same objective causes false promotion pressure.

## Recurrence signal

This issue is present when:
- regrouped candidate selection is happening after decomposition
- a narrow candidate looks strong under one focus profile
- but the current experiment actually needs wider dashboard semantics

## Current workaround

Score regrouped candidates under at least:
- one current objective profile
- one contrast profile

Then record both winners and keep the mainline recommendation attached to the current objective only.

## Structural fix candidate

Make objective-profile scoring a required stage between regrouping and re-entry decisions for compound analytical figures.

## Current proven example

- `image4`
- dashboard winner: `full_dashboard`
- table-focus winner: `title_plus_table`
