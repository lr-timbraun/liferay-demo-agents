---
name: demo-planning
description: Ingesting client briefs, discovering brand identities, and co-creating live click-by-click presenter storyboards in close collaboration with the User.
---

# Skill: Demo Planning (Orchestrator co-creation)

## Description
This skill defines the structured collaborative process used by the Conductor to discover corporate brand details, interview the User, and author the locked presenter storyboard (`DEMO_PLAN.md`) and the technical implementation ledger (`IMPLEMENTATION_PLAN.md`).

---

## Strict Execution Protocol (Mandatory Reads)

You MUST NOT attempt to run any planning loops or interview the User from memory. You MUST load and read these files BEFORE entering the Strategy or Execution phase:
- **Demo Plan Template**: `templates/DEMO_PLAN.template.md` (Defines the standard click-by-click storyboard outline).
- **Implementation Plan Template**: `templates/IMPLEMENTATION_PLAN.template.md` (Defines the standard technical DAG tracking ledger).

---

## Collaborative Planning Workflow Steps

### Step 1: Brand & Objective Discovery
- Crawl and headlessly inspect the customer's actual corporate website to extract their branding parameters (primary color HEX, secondary accent HEX, logo paths, typography families, and business industry context).
- Ask the User (SE) targeted, high-signal multiple-choice questions to confirm their presentation goals, targeted products, and desired workflow sequences.

### Step 2: Presenter Storyboard Co-Creation
- Co-create a locked, click-by-click storyboard (`DEMO_PLAN.md` based on `templates/DEMO_PLAN.template.md`) which details each scene, standard talking points (bulleted, non-scripted), the expected visual outcomes, and timestamped Visual Receipt Checkpoint image targets.

### Step 3: Technical Implementation Plan Initialization
- Co-draft the technical checklist (`IMPLEMENTATION_PLAN.md` based on `templates/IMPLEMENTATION_PLAN.template.md`) mapping the DAG execution sequence, defining what custom Objects, fragments, page templates, workflows, or client extensions must be built, compiled, and deployed by the swarm to support the storyboard scenes.
- **Fragment Modularity Mandate (CRITICAL):** Custom Page Fragments MUST be designed as highly modular, single elements of a page (such as a Hero Banner, a specific Product Card, a Testimonial, or a dynamic Feature block). You are strictly forbidden from planning or creating "full page fragments" or bundling an entire page layout into a single monolithic fragment. A proper Liferay page is constructed by dragging and dropping multiple small, reusable modular fragments onto the layout canvas, not by rendering a single full-page fragment.

---

## Available Resources
- Demo Plan Template: `templates/DEMO_PLAN.template.md`
- Implementation Plan Template: `templates/IMPLEMENTATION_PLAN.template.md`
