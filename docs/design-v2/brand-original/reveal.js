    // 1. Reveal on scroll
    function initRevealAnimations() {
        var els = document.querySelectorAll('.rv');
        if (!els.length) return;

        if (!('IntersectionObserver' in window)) {
            els.forEach(function (e) {
                e.classList.add('in');
            });
            return;
        }

        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (x) {
                if (x.isIntersecting) {
                    x.target.classList.add('in');
                    io.unobserve(x.target);
                }
            });
        }, {
            threshold: 0.12,
            rootMargin: '0px 0px -40px 0px'
        });

        els.forEach(function (e, i) {
            e.style.transitionDelay = (i % 4 * 70) + 'ms';
            io.observe(e);
        });
    }

