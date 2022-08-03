var div = document.querySelectorAll('div.chartwrapper');
[...div].forEach((data) => {
    if (data === '') {
        data.parentNode.style.display = 'none';
        //or add a class that hides the element
    }
});