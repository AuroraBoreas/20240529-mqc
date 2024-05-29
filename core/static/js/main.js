// function updateProgressbar() {
//     const scrollHeight = document.documentElement.scrollHeight;
//     const progress = `${window.scrollY / (scrollHeight - window.innerHeight) * 100}%`;
//     console.log(progress);
//     document.querySelector('#progressbar').style.setProperty('--progressbar', progress);
// }

$(function() {
    $(".datepicker").datepicker({
        dateFormat: "yy-mm-dd"
    });
});

// document.addEventListener('scroll', updateProgressbar);
