// Görgetés az adott szolgáltatáshoz oldalirányban
function scrollToService(serviceName) {
    const container = document.querySelector('.csomagcontent'); // Görgethető konténer
    if (!container) {
        console.error("A '.csomagcontent' container nem található.");
        return;
    }

    // A cél elem keresése a containeren belül
    const targetElement = container.querySelector(`#${serviceName}`);
    if (!targetElement) {
        console.error(`A cél elem '${serviceName}' nem található.`);
        return;
    }

    // Görgetés oldalirányban
    container.scrollTo({
        left: targetElement.offsetLeft - container.offsetLeft, // Az elem vízszintes pozíciójának számítása
        behavior: 'smooth', // Sima görgetés
    });
}

