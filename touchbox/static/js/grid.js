window.addEventListener("load", () => {
    [...document.querySelectorAll(".box")].forEach((el) => {
        const util = new SetData(el);
        util.classSet();
        util.classText();
    });
});

class SetData {
    #firstColor = "first-color";
    #secondColor = "second-color";
    #thirdColor = "third-color";
    #fourthColor = "fourth-color";
    #element;
    #text;

    constructor(element) {
        this.#element = element;
        this.#text = element.innerHTML;
    }

    get element() {
        return this.#element;
    }

    classSet() {
        if (0 < this.#text && this.#text <= 25) {
            this.element.classList.add("first-color");
        }
        if (25 < this.#text && this.#text <= 50) {
            this.element.classList.add("second-color");
        }
        if (50 < this.#text && this.#text <= 75) {
            this.element.classList.add("third-color");
        }
        if (75 < this.#text && this.#text <= 100) {
            this.element.classList.add("fourth-color");
        }
    }

    classText() {
        this.element.innerHTML = `${this.element.innerHTML}%`;
    }
}