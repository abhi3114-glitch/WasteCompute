import { animate, stagger, spring, inView } from "https://cdn.skypack.dev/motion";

// Cinematic Easing
const EASE_CINEMATIC = [0.16, 1, 0.3, 1]; // "Apple" ease

document.addEventListener("DOMContentLoaded", () => {
    // Header Fade In (Slow)
    animate("header", { y: [-20, 0], opacity: [0, 1] }, { duration: 1.2, easing: EASE_CINEMATIC });

    // Staggered Hero Elements (Slower delay, longer duration)
    animate(
        ".hero > *",
        { y: [30, 0], opacity: [0, 1] },
        { delay: stagger(0.2), duration: 1.5, easing: EASE_CINEMATIC }
    );

    // Dashboard Cards Stagger
    if (document.querySelector(".container")) {
        animate(
            ".card, .section-title",
            { y: [40, 0], opacity: [0, 1] },
            { delay: stagger(0.15), duration: 1.0, easing: EASE_CINEMATIC }
        );
    }
});

// Interactive Elements - physical but subtle
const buttons = document.querySelectorAll(".btn");
buttons.forEach(btn => {
    btn.addEventListener("mouseenter", () => {
        animate(btn, { scale: 1.03 }, { duration: 0.4, easing: "ease-out" });
    });
    btn.addEventListener("mouseleave", () => {
        animate(btn, { scale: 1 }, { duration: 0.4, easing: "ease-out" });
    });
});
