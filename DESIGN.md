---
name: Safety-First Automotive System
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#baccb0'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#85967c'
  outline-variant: '#3c4b35'
  surface-tint: '#2ae500'
  primary: '#efffe3'
  on-primary: '#053900'
  primary-container: '#39ff14'
  on-primary-container: '#107100'
  inverse-primary: '#106e00'
  secondary: '#ffe2ab'
  on-secondary: '#402d00'
  secondary-container: '#ffbf00'
  on-secondary-container: '#6d5000'
  tertiary: '#fff8f7'
  on-tertiary: '#690006'
  tertiary-container: '#ffd3ce'
  on-tertiary-container: '#c50015'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#79ff5b'
  primary-fixed-dim: '#2ae500'
  on-primary-fixed: '#022100'
  on-primary-fixed-variant: '#095300'
  secondary-fixed: '#ffdfa0'
  secondary-fixed-dim: '#fbbc00'
  on-secondary-fixed: '#261a00'
  on-secondary-fixed-variant: '#5c4300'
  tertiary-fixed: '#ffdad6'
  tertiary-fixed-dim: '#ffb4ab'
  on-tertiary-fixed: '#410002'
  on-tertiary-fixed-variant: '#93000c'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-alert:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '500'
    lineHeight: '1.5'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.08em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  touch-margin: 24px
  gutter: 16px
  safe-area: 40px
---

## Brand & Style

The design system is engineered for high-stakes automotive environments where cognitive load management and immediate legibility are paramount. The brand personality is rooted in technical precision, reliability, and proactive safety. It evokes a sense of a "digital co-pilot"—unobtrusive when operations are normal, but authoritative and urgent when a risk is detected.

The design style utilizes a **High-Contrast Industrial** approach. It blends modern minimalism with tactile functional elements reminiscent of performance vehicle telemetry. By prioritizing dark surfaces and vibrant, meaningful accents, the system ensures that the driver's attention is only diverted for the minimum time necessary to process critical information.

## Colors

The palette is strictly functional, adhering to a "dark room" philosophy to eliminate cabin glare and preserve the driver's night vision. 

- **Base Surfaces:** Use a deep charcoal (#121212) and true black (#000000) to create depth and hide hardware bezels.
- **Neon Green (Safe):** Used exclusively for active monitoring and "all-clear" states.
- **Vibrant Amber (Warning):** Reserved for early-stage drowsiness detection and non-critical system notifications.
- **Pulsing Red (Critical):** Used for immediate intervention alerts. This color should occupy the largest visual area only during emergencies.
- **Neutral Grays:** Used for secondary labels and inactive UI borders to ensure they recede into the background.

## Typography

This design system utilizes **Inter** for its exceptional legibility and neutral, technical character. Typography is used as a primary hierarchy tool, emphasizing "glanceability"—the ability to read and comprehend data in under 0.5 seconds.

- **Weight as Information:** Bold and Extra Bold weights are used for status readings to ensure they remain crisp against dark backgrounds.
- **Uppercase Labels:** Used for technical metadata and secondary telemetry to distinguish them clearly from primary instructional text.
- **Scale:** Font sizes are oversized compared to mobile or desktop standards to compensate for arm-length viewing and vehicle vibration.

## Layout & Spacing

The layout follows a **Fluid Grid** model optimized for horizontal automotive displays. It prioritizes "Safe Zones" located within the driver's primary line of sight.

- **Rhythm:** An 8px base unit governs all dimensions. 
- **Touch Targets:** Interactive elements must maintain a minimum hit area of 64px to ensure accuracy while the vehicle is in motion.
- **Visual Breathing Room:** Generous margins (40px+) are applied to the edges of the screen to prevent UI elements from being obscured by steering wheels or dashboard trim.
- **Information Density:** High density is permitted for technical telemetry, but critical alerts must utilize a "Takeover" layout that clears the screen of all non-essential data.

## Elevation & Depth

Hierarchy is established through **Tonal Layers** and subtle **Inner Glows** rather than traditional drop shadows.

- **Surface Tiers:** The background is #000000. Primary containers use #1A1A1A. Elevated interactive cards use #262626.
- **Luminance:** Depth is conveyed by the brightness of the accent color. A "Safe" state might have a subtle 2px Neon Green outer glow to make the element appear to emit light, mimicking a physical cockpit instrument.
- **Recession:** Inactive or background information is dimmed to 40-60% opacity to ensure it does not compete with active monitoring data.

## Shapes

The design system employs **Soft (Level 1)** roundedness to maintain an industrial, tool-like aesthetic. 

- **Corner Radius:** 4px (0.25rem) is the standard for most components, providing a professional edge that feels more precise than overly rounded "consumer" electronics. 
- **Industrial Accents:** Beveled edges or 45-degree chamfered corners may be used for status indicators to reinforce the automotive/hardware metaphor.
- **Gauges:** Circular elements are permitted for telemetry, but they should be framed within rectangular containers to maintain grid alignment.

## Components

Components are designed for "eyes-on-the-road" safety.

- **Industrial Gauges:** Use semi-circular progress bars for fatigue levels. The stroke weight should be thick (8px+) with high-contrast color segments.
- **Action Buttons:** Large, full-width or half-width blocks. They must use high-contrast fills (e.g., a solid Green button with Black text) for primary actions like "I'M AWAKE."
- **Status Indicators:** Small, pill-shaped chips that use steady or pulsing lights. A "Safe" pulse should be slow and rhythmic, while a "Critical" pulse is rapid and jarring.
- **Alert Overlays:** Modal-style takeovers that dim the background to 90% black. They feature massive centered icons and high-weight display typography.
- **List Items:** High-row height (72px+) with clear separators to prevent mis-taps. Each row should contain one primary metric and one label.
- **Touch-Friendly Sliders:** Used for system volume or brightness, featuring an oversized thumb handle that is easy to grab without looking directly at the screen.