# 🚀 Anime Star Fighter Recipe
## 40-Iteration Workflow for High-Quality 3D Models

---

## 📋 Overview

**Total Iterations:** 40 (10 base + 30 refinement)
**Software:** Blender 4.2.3 LTS with Python scripting
**Output:** glTF 2.0 for Three.js viewer
**Style:** Low-poly anime/mecha aesthetic

---

## 🎯 PHASE 1: FOUNDATION (Iterations 1-10)

### Iteration 1: Base Structure
**Goal:** Establish primary silhouette
- Create split fuselage (upper/lower halves)
- Define overall proportions (12×12×4 envelope)
- **Key Insight:** Split bodies add visual interest vs single block

### Iteration 2: Nose Section
**Goal:** Define front profile
- Pointed nose cone with progressive taper
- Add V-fin detail (Gundam-style headpiece)
- **Key Insight:** V-fin instantly reads as "mecha"

### Iteration 3: Body Core
**Goal:** Midsection detail
- Connecting spine between fuselage halves
- Intake vents on sides
- **Key Insight:** Break up flat surfaces with functional-looking details

### Iteration 4: Transitions
**Goal:** Connect sections smoothly
- Section collars (front/rear)
- Gap filling between nose and body
- **Key Insight:** Transitions prevent "floating part" look

### Iteration 5: Undercarriage
**Goal:** Bottom surface interest
- Belly pan
- Landing gear bays (suggested, not detailed)
- **Key Insight:** Model must look good from all angles

### Iteration 6: Wing Roots
**Goal:** Wing attachment
- Wing root fillets and fairings
- Blend wing into body
- **Key Insight:** Smooth transitions = professional look

### Iteration 7: Wing Main
**Goal:** Primary wing shape
- Forward-swept wing extensions (distinctive!)
- Custom profile using bmesh
- **Key Insight:** Forward sweep = aggressive, distinctive silhouette

### Iteration 8: Stabilizers
**Goal:** Rear silhouette
- Twin vertical stabilizers
- Tip lights
- **Key Insight:** Twin tails = iconic mecha look (Gundam, Macross)

### Iteration 9: Engines
**Goal:** Propulsion systems
- Engine nacelles with intake lips
- Nozzles and thrusters
- **Key Insight:** Engines need "suck, squeeze, bang, blow" visual story

### Iteration 10: Cockpit
**Goal:** Pilot visibility
- Bubble canopy with frame
- Frame segments
- **Key Insight:** Canopy = human scale reference

---

## 🎨 PHASE 2: DISTINCTIVE SHAPES (Iterations 11-20)

### Iteration 11: Surface Detail
**Goal:** Break up large surfaces
- Panel lines (horizontal and vertical)
- **Key Insight:** Panel lines add manufactured look without geometry cost

### Iteration 12: Panel Lines
**Goal:** Manufacturing detail
- Recessed panel lines
- Rivet heads at intersections
- **Key Insight:** Less is more - don't over-rivet

### Iteration 13: Weapons
**Goal:** Combat capability
- Wing hardpoints
- Weapon pylons and barrels
- **Key Insight:** Weapons add purpose to design

### Iteration 14: Sensors
**Goal:** Technical functionality
- Sensor domes (ico spheres)
- Side arrays
- **Key Insight:** Sensors add "tech" aesthetic

### Iteration 15: Antennae
**Goal:** Communication
- Main dorsal antenna
- Side comm arrays
- **Key Insight:** Thin cylinders add vertical interest

### Iteration 16: Decals
**Goal:** Identity markings
- Stripe decals on body
- Roundels/markings
- **Key Insight:** Decals add color breaks without new materials

### Iteration 17: Weathering
**Goal:** Realism
- Exhaust stains near nozzles
- Soot marks
- **Key Insight:** Subtle weathering adds story

### Iteration 18: Trim
**Goal:** Material contrast
- Chrome/running trim on leading edges
- Edge highlighting
- **Key Insight:** Shiny trim catches light

### Iteration 19: Transparency
**Goal:** See-through elements
- Side canopy windows
- Lens elements
- **Key Insight:** Glass breaks up opaque surfaces

### Iteration 20: Navigation Lights
**Goal:** Safety/realism
- Red port (left), Green starboard (right)
- Emissive materials
- **Key Insight:** Real aviation convention adds authenticity

---

## 🛠️ PHASE 3: MATERIALS (Iterations 21-30)

### Iteration 21: Mechanicals
**Goal:** Functional detail
- Gunmetal hinges and joints
- Actuator housings
- **Key Insight:** Mechanical = believable

### Iteration 22: Seals
**Goal:** Construction realism
- Canopy seals
- Gasket details
- **Key Insight:** Seals imply pressurization

### Iteration 23: Warnings
**Goal:** Operational detail
- Warning stripes (yellow/black)
- Caution markings
- **Key Insight:** Safety markings add lived-in feel

### Iteration 24: Heat Protection
**Goal:** Aerodynamic realism
- Heat-resistant belly tiles
- Thermal protection
- **Key Insight:** Function informs form

### Iteration 25: Identification
**Goal:** Unit markings
- Name plates
- Serial numbers (implied)
- **Key Insight:** Identity implies larger universe

### Iteration 26: Scale Check
**Goal:** Proportional review
- Verify all parts fit in 12×12×4 envelope
- Check silhouette from front/top/side
- **Key Insight:** Walk around virtual model

### Iteration 27: Balance
**Goal:** Visual weight distribution
- Dorsal spine for top/bottom balance
- Symmetry check
- **Key Insight:** Asymmetry should be intentional

### Iteration 28: Detail Distribution
**Goal:** Even complexity
- Scatter rivets evenly
- Distribute greebles
- **Key Insight:** Avoid detail clustering

### Iteration 29: Final Gap Fill
**Goal:** Clean construction
- Blend pieces between sections
- Fill remaining gaps
- **Key Insight:** No floating parts

### Iteration 30: Lighting
**Goal:** Presentation ready
- 4-point anime lighting (key, fill, rim, under)
- Engine glow lights
- World setup
- **Key Insight:** Anime lighting = warm key + cool fill + warm rim

---

## ✨ PHASE 4: COHESIVENESS (Iterations 31-40)

### Iteration 31: Material Unification
- Ensure material colors harmonize
- Check metallic values across parts

### Iteration 32: Edge Consistency
- Verify edge split angles
- Smooth vs sharp edge balance

### Iteration 33: Scale Relationships
- Check weapon size vs body
- Verify cockpit fits pilot

### Iteration 34: Visual Flow
- Lead eye from nose to tail
- Ensure no visual dead ends

### Iteration 35: Silhouette Polish
- View from 45° angles
- Check against pure black background

### Iteration 36: Detail Hierarchy
- Primary (wings, body) → Secondary (panel lines) → Tertiary (rivets)
- Ensure clear hierarchy

### Iteration 37: Color Balance
- Primary: 60% (body)
- Secondary: 30% (accents)
- Accent: 10% (lights, small details)

### Iteration 38: Function Check
- Ask: "Does this part do something?"
- Remove or justify purely decorative elements

### Iteration 39: Story Elements
- Add one "hero" detail (special sensor, unique weapon)
- Make something stand out

### Iteration 40: Final Export
- Camera setup for hero shot
- glTF export with materials
- Render preview

---

## 🎨 MATERIAL PALETTE

| Name | Color | Metallic | Roughness | Use |
|------|-------|----------|-----------|-----|
| Body_Primary | (0.08, 0.22, 0.55) | 0.7 | 0.3 | Main fuselage |
| Body_Secondary | (0.92, 0.93, 0.95) | 0.1 | 0.4 | Armor plates |
| Accent_Red | (0.92, 0.15, 0.12) | 0.4 | 0.3 | Vents, lights |
| Accent_Yellow | (1.0, 0.75, 0.15) | 0.6 | 0.25 | V-fin, sensors |
| Dark_Panel | (0.12, 0.14, 0.18) | 0.3 | 0.6 | Panels, vents |
| Cockpit | (0.02, 0.05, 0.12) | 0.9 | 0.05 | Glass |
| Engine_Glow | Emission (0.2, 0.8, 1.0) | - | - | Thrusters |
| Gunmetal | (0.25, 0.27, 0.3) | 0.8 | 0.35 | Mechanicals |

---

## 💡 KEY INSIGHTS

1. **Gap Filling:** Every transition needs consideration - floating parts break immersion

2. **Distinctive Shapes:** The forward-swept wings and twin tails make this memorable

3. **Material Variety:** 8 materials gives complexity without overwhelming

4. **Anime Lighting:** Warm key + cool fill + warm rim = classic anime look

5. **Silhouette First:** If it reads as a star fighter in pure black, the details will enhance

6. **Hierarchy:** Primary forms → Secondary details → Tertiary small stuff

7. **Function Sells Fantasy:** Every detail should imply purpose

---

## 🚀 QUICK START TEMPLATE

```python
# PHASE 1-10: Foundation
def create_foundation():
    # 1. Split fuselage
    # 2. Nose + V-fin
    # 3. Intakes
    # 4. Collars
    # 5. Belly
    # 6. Wing roots
    # 7. Wings
    # 8. Stabilizers
    # 9. Engines
    # 10. Cockpit
    pass

# PHASE 11-20: Details
def add_distinctive_shapes():
    # 11-12. Panel lines
    # 13. Weapons
    # 14-15. Sensors/antennae
    # 16-20. Decals/weathering/lights
    pass

# PHASE 21-30: Materials
def refine_materials():
    # 21-25. Mechanicals/seals/warnings/tiles/ID
    # 26-30. Polish + lighting
    pass

# PHASE 31-40: Cohesion
def final_pass():
    # Check, check, check
    # Export
    pass
```

---

## 📊 FINAL STATS

- **Polygons:** ~2,400
- **Materials:** 8
- **Emissive Elements:** 3 (engines, nav lights)
- **Distinctive Features:** Forward wings, twin tails, V-fin
- **Render Time:** ~13 seconds (512 samples)

---

## 🎯 NEXT LEVEL IDEAS

- **Weathering V2:** Panel line grime, scratches, chipped paint
- **Animation:** Landing gear deployment, wing sweep
- **Variants:** Interceptor (larger engines), Bomber (weapon pods)
- **Cockpit Interior:** Seat, controls, HUD
- **Damage States:** Wing damage, scorched panels

---

**Remember:** The first 10 get you a model. The next 30 make it *good*.
