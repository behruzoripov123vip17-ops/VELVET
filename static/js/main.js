(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });
    

    // Date and time picker
    $('.date').datetimepicker({
        format: 'L'
    });
    $('.time').datetimepicker({
        format: 'LT'
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        margin: 30,
        dots: true,
        loop: true,
        center: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });
    

    // Japanese ambient site audio.
    // Browsers can block audible autoplay; in that case the first user interaction
    // starts the music automatically. The toggle remains available at all times.
    $(document).ready(function () {
        const audio = document.getElementById('jp-site-audio');
        const toggle = document.getElementById('jp-audio-toggle');
        if (!audio || !toggle) return;

        audio.volume = 0.28;

        const syncAudioUi = function () {
            const playing = !audio.paused;
            toggle.classList.toggle('paused', !playing);
            toggle.setAttribute('aria-pressed', String(playing));
            toggle.setAttribute('aria-label', playing ? 'Turn music off' : 'Turn music on');
            toggle.title = playing ? 'Pause music' : 'Play music';
            toggle.innerHTML = playing
                ? '<i class="fas fa-volume-up"></i>'
                : '<i class="fas fa-volume-mute"></i>';
        };

        const startAudio = function () {
            const promise = audio.play();
            if (promise && typeof promise.catch === 'function') {
                promise.catch(function () {
                    // Audible autoplay was blocked by the browser.
                    syncAudioUi();
                });
            }
            syncAudioUi();
        };

        toggle.addEventListener('click', function (event) {
            event.preventDefault();
            if (audio.paused) {
                startAudio();
            } else {
                audio.pause();
                syncAudioUi();
            }
        });

        ['pointerdown', 'keydown', 'touchstart'].forEach(function (eventName) {
            document.addEventListener(eventName, function () {
                if (audio.paused) startAudio();
            }, { once: true, passive: true });
        });

        audio.addEventListener('play', syncAudioUi);
        audio.addEventListener('pause', syncAudioUi);
        audio.addEventListener('error', function () {
            toggle.classList.add('paused');
            toggle.setAttribute('aria-label', 'Music unavailable');
            toggle.title = 'Music unavailable';
        });

        // Attempt audible autoplay immediately after the page is ready.
        startAudio();
    });

})(jQuery);
