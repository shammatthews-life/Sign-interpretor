# Phase H25 Right Sidebar Design & Architecture Audit

**Target Component:** Browser Extension Right-Sidebar Overlay (`extension/content/overlay.js`, `overlay.css`)  
**Host Environment:** YouTube Video Viewport & Showcase (`tools/test_right_sidebar_showcase.html`)  
**Design Paradigm:** Premium AI Accessibility Tool with Deep Obsidian Glassmorphism & Bottom-Right 3D Avatar Dock  

---

## 1. Existing Architecture Review (Phase H24 Baseline)

The Phase H24 implementation transitioned the extension from a simple floating box to a docked sidebar:
- **Mount Point:** Isolated via Shadow DOM (`#isl-accessibility-overlay-root`) preventing any style leakage into YouTube's DOM or vice-versa.
- **Right Sidebar Anchor:** `position: fixed; top: 0; right: 0; bottom: 0; width: 380px; height: 100vh;` with deep obsidian glass (`rgba(10, 14, 22, 0.96)`, `backdrop-filter: blur(32px)`).
- **YouTube Viewport Offset:** Dynamically shifts `#primary` / `ytd-watch-flexy` left by `margin-right: 380px` during sidebar mode so the video player is never occluded.
- **Bottom-Right Aether Dock:** `#isl-bottom-avatar-dock` pins the 3D WebGL viewport (`#isl-aether-container`) in the bottom-right corner, framing Aether in a TV-interpreter broadcast layout.
- **Collapsible Edge Handle:** When collapsed, slides smoothly off-screen (`transform: translateX(100%)`), leaving a vertical pill (`#isl-sidebar-toggle-handle` labeled `🤟 ISL BAR`).
- **Layout Switcher:** Dedicated button (`btn-layout-mode`) allows switching between full-height Right Sidebar Dock and Floating Window mode.

---

## 2. Refinements Identified for Phase H25 Elevation

| Area | Current State | Phase H25 Elevation Plan |
|:---|:---|:---|
| **Visual Lighting & Rim Accent** | Subtle cyan border | Electric-cyan glowing edge backlight with gradient border highlights (`rgba(56, 189, 248, 0.5)`). |
| **Aether Avatar Dock Framing** | 220px fixed viewport | Studio-grade glass bezel with dual neon indicator badge (`[3D AETHER INTERPRETER • 60 FPS]`), pulsing green status dot, and active motion telemetry. |
| **Subtitle Fallback Pill** | Embedded below avatar | High-contrast crimson glass pill (`rgba(220, 38, 38, 0.25)`) with monospace typography and readable 2500 ms persistence timer. |
| **Responsive Viewports** | Desktop 1080p tested | Seamless adaptation down to 1366×768, 1280×720, and mobile drawers with compact video offset scaling. |
| **Accessibility & Keyboard Focus** | Mouse-driven controls | High-visibility focus rings (`:focus-visible`), aria labels on all interactive buttons, and screen-reader status announcements. |

---

## 3. Preserved Operational Invariants

1. **Zero Style Contamination:** Shadow DOM boundary strictly preserved.
2. **Single Authoritative Avatar Runtime:** Exactly one Three.js WebGL canvas and `SignScheduler` instance.
3. **No Decorative Non-Functional Buttons:** Every control button triggers a real, verified pipeline action.
