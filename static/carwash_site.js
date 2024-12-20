document.addEventListener("DOMContentLoaded", function () {
    const kozmetika = document.querySelector(".kozmetika"); // A fő scrollable konténer
    const containers = document.querySelectorAll(".kozmetikaOuterContainer"); // Az elemek
    const mobileScroller = document.querySelector(".MobileScroller"); // A radio button konténer

    // Töröljük az esetlegesen már ott lévő gombokat
    mobileScroller.innerHTML = "";

    // Létrehozunk annyi radio buttont, ahány elem van
    containers.forEach((container, index) => {
        const radioButton = document.createElement("input");
        radioButton.type = "radio";
        radioButton.name = "scrollRadio";
        radioButton.id = `radio-${index}`;
        radioButton.classList.add("radioButton");
        if (index === 0) radioButton.checked = true; // Az első legyen alapból kijelölve

        // Kinyerjük a cím szövegét
        const titleElement = container.querySelector(".KozmetikaCim");
        const titleText = titleElement ? titleElement.textContent : `Elem ${index + 1}`;

        // Létrehozzuk a labelt és beállítjuk a szövegét
        const label = document.createElement("label");
        label.classList.add("mobileScrollerLabel")
        label.setAttribute("for", `radio-${index}`);
        label.textContent = titleText; // A containeren belüli cím lesz a szöveg

        // Hozzáadjuk a radio button-t és a label-t a MobileScrollerhez
        mobileScroller.appendChild(radioButton);
        mobileScroller.appendChild(label);

        // Görgetési esemény hozzáadása a radio buttonhoz
        radioButton.addEventListener("change", function () {
            const scrollPosition = container.offsetLeft; // Az elem pozíciója balról
            console.log(scrollPosition)
            kozmetika.scrollTo({
                left: scrollPosition,
                behavior: "smooth" // Sima görgetés
            });
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const kozmetika = document.querySelector(".kozmetika"); // A fő scrollable konténer
    const containers = document.querySelectorAll(".kozmetikaOuterContainer"); // Az elemek
    const mobileScroller = document.getElementById("MobileScrollerKozmetika"); // A radio button konténer

    // Töröljük az esetlegesen már ott lévő gombokat
    mobileScroller.innerHTML = "";

    // Létrehozunk annyi radio buttont, ahány elem van
    containers.forEach((container, index) => {
        const radioButton = document.createElement("input");
        radioButton.type = "radio";
        radioButton.name = "scrollRadio";
        radioButton.id = `radio-${index}`;
        radioButton.classList.add("radioButton");
        if (index === 0) radioButton.checked = true; // Az első legyen alapból kijelölve

        // Kinyerjük a cím szövegét
        const titleElement = container.querySelector(".KozmetikaCim");
        const titleText = titleElement ? titleElement.textContent : `Elem ${index + 1}`;

        // Létrehozzuk a labelt és beállítjuk a szövegét
        const label = document.createElement("label");
        label.classList.add("mobileScrollerLabel")
        label.setAttribute("for", `radio-${index}`);
        label.textContent = titleText; // A containeren belüli cím lesz a szöveg

        // Hozzáadjuk a radio button-t és a label-t a MobileScrollerhez
        mobileScroller.appendChild(radioButton);
        mobileScroller.appendChild(label);

        // Görgetési esemény hozzáadása a radio buttonhoz
        radioButton.addEventListener("change", function () {
            const scrollPosition = container.offsetLeft; // Az elem pozíciója balról
            console.log(scrollPosition)
            kozmetika.scrollTo({
                left: scrollPosition,
                behavior: "smooth" // Sima görgetés
            });
        });
    });
});

function scrollToService(serviceId) {
    console.log(serviceId)
    const targetElement = document.getElementById(serviceId);
    console.log(targetElement)
    if (targetElement) {
        targetElement.scrollIntoView({
            behavior: 'smooth', // Smooth scrolling effect
            block: 'nearest',  // Ensures the container scrolls sideways
            inline: 'start'    // Align the element to the start (left side)
        });
    } else {
        console.error(`Element with ID '${serviceId}' not found.`);
    }
}