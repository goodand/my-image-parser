# Repeated Task: Owner-Family Routing Status Enum Hardening

## Pattern Name

Owner-Family Routing Status Enum Hardening

## Trigger

- A family map for an owner skill needs to classify surfaces as canonical, adjacent-but-routed, or consumer-only
- Different documents in the same owner-family set are using different labels for the same routing classification
- A review pass found a 4th or 5th value being used inconsistently alongside the 3 canonical values

## Stable Steps

1. Define exactly 3 enum values for the `Lifecycle Routing Status` column:
   - `canonical` — primary surface is a vendored tool under the owner's primary charter path
   - `temporarily routed adjacent` — primary surface is a non-vendored or adjacent tool; lifecycle routes here by convention, not primary charter
   - `consumer-only` — no lifecycle dependency on the owner's managed surfaces; the skill only consumes outputs
2. Write a legend for these values in the family map that describes the *surface*, not the skill: "describes the ownership status of the Primary Lifecycle Surface for each row, not the skill itself."
3. Update every row in the consumer table to use exactly one of these 3 values.
4. Remove any compound values (e.g., `canonical + note`); move note content into a separate inline cell annotation or footnote.
5. Verify that the routing decision tree's branches use the same enum labels as the table (e.g., `Lifecycle Routing Status: canonical` in the branch label).
6. Verify that the quick pre-routing check's steps map 1:1 to the 3 enum values.

## Candidate Promotion

- Checklist: 3-point enum consistency check (table values, legend, routing tree, pre-routing check all use same 3 strings)
- Linter rule: scan family-map markdown for any Lifecycle Routing Status cell that is not one of the 3 canonical values
- Skill: owner-family vocabulary audit helper that reads the family map and reports any enum drift
