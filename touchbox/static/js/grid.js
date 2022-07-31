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
        if (0.0 === this.#text) {
            this.element.classList.add("default-color");
        }
        if (0 < this.#text && this.#text <= 10) {
            this.element.classList.add("first-color");
        }
        if (10 < this.#text && this.#text <= 20) {
            this.element.classList.add("second-color");
        }
        if (20 < this.#text && this.#text <= 30) {
            this.element.classList.add("third-color");
        }
        if (30 < this.#text && this.#text <= 40) {
            this.element.classList.add("fourth-color");
        }
        if (40 < this.#text && this.#text <= 50) {
            this.element.classList.add("fifth-color");
        }
        if (50 < this.#text && this.#text <= 60) {
            this.element.classList.add("sixth-color");
        }
        if (60 < this.#text && this.#text <= 70) {
            this.element.classList.add("seventh-color");
        }
        if (70 < this.#text && this.#text <= 80) {
            this.element.classList.add("eighth-color");
        }
        if (80 < this.#text && this.#text <= 90) {
            this.element.classList.add("ninth-color");
        }
        if (90 < this.#text && this.#text <= 100) {
            this.element.classList.add("tenth-color");
        }
    }

    classText() {
        this.element.innerHTML = `${this.element.innerHTML}%`;
    }
}