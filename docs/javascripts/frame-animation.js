function initialiseFrameAnimations() {
  document.querySelectorAll(".frame-animation").forEach((player) => {
    if (player.dataset.initialised === "true") {
      return;
    }

    player.dataset.initialised = "true";

    const image = player.querySelector(".frame-animation-image");
    const toggleButton = player.querySelector('[data-action="toggle"]');
    const previousButton = player.querySelector('[data-action="previous"]');
    const nextButton = player.querySelector('[data-action="next"]');
    const counter = player.querySelector(".frame-animation-counter");

    const frames = player.dataset.images
      .split("|")
      .map((path) => path.trim())
      .filter(Boolean);

    const interval = Number(player.dataset.interval) || 1000;

    let currentFrame = 0;
    let timer = null;
    let playing = true;

    // Preload all frames.
    frames.forEach((source) => {
      const preload = new Image();
      preload.src = source;
    });

    function showFrame(index) {
      currentFrame = (index + frames.length) % frames.length;
      image.src = frames[currentFrame];
      counter.textContent = `${currentFrame + 1} / ${frames.length}`;
    }

    function start() {
      window.clearInterval(timer);

      timer = window.setInterval(() => {
        showFrame(currentFrame + 1);
      }, interval);

      playing = true;
      toggleButton.textContent = "Pause";
    }

    function pause() {
      window.clearInterval(timer);
      timer = null;
      playing = false;
      toggleButton.textContent = "Play";
    }

    toggleButton.addEventListener("click", () => {
      if (playing) {
        pause();
      } else {
        start();
      }
    });

    previousButton.addEventListener("click", () => {
      pause();
      showFrame(currentFrame - 1);
    });

    nextButton.addEventListener("click", () => {
      pause();
      showFrame(currentFrame + 1);
    });

    showFrame(0);
    start();
  });
}

// Supports MkDocs Material instant navigation.
if (typeof document$ !== "undefined") {
  document$.subscribe(initialiseFrameAnimations);
} else {
  document.addEventListener("DOMContentLoaded", initialiseFrameAnimations);
}
