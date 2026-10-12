/**
 * Italy Legal Entry - Main JavaScript interactions
 */

(function () {
    'use strict';

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

    // 2. Sticky Navbar scroll elevation
    function initNavScroll() {
        var nav = document.getElementById('site-navigation');
        if (!nav) return;

        window.addEventListener('scroll', function () {
            if (window.scrollY > 20) {
                nav.classList.add('is-scrolled');
            } else {
                nav.classList.remove('is-scrolled');
            }
        }, { passive: true });
    }

    // 3. Mobile Navigation Drawer
    function initMobileNav() {
        var burger = document.getElementById('burger-btn');
        var drawer = document.getElementById('mobile-nav');
        var closeBtn = document.getElementById('mobile-nav-close');
        var mobLinks = document.querySelectorAll('.mob-link');

        if (!burger || !drawer) return;

        function openDrawer() {
            drawer.classList.add('open');
            drawer.setAttribute('aria-hidden', 'false');
            burger.setAttribute('aria-expanded', 'true');
            document.body.style.overflow = 'hidden';
        }

        function closeDrawer() {
            drawer.classList.remove('open');
            drawer.setAttribute('aria-hidden', 'true');
            burger.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
        }

        burger.addEventListener('click', openDrawer);
        if (closeBtn) closeBtn.addEventListener('click', closeDrawer);

        mobLinks.forEach(function (link) {
            link.addEventListener('click', closeDrawer);
        });

        drawer.addEventListener('click', function (e) {
            if (e.target === drawer) closeDrawer();
        });
    }

    // 4. Modal System (Parcours & Enterprise)
    function initModals() {
        var triggers = document.querySelectorAll('[data-open-modal]');
        var closers = document.querySelectorAll('[data-close-modal]');

        triggers.forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                var targetId = 'modal-' + btn.getAttribute('data-open-modal');
                var modal = document.getElementById(targetId);
                var preselect = btn.getAttribute('data-preselect');

                if (preselect && modal) {
                    var radio = modal.querySelector('input[name="ile_goal"][value="' + preselect + '"]');
                    if (radio) {
                        radio.checked = true;
                        updateRadioCardStyles(modal);
                    }
                }

                if (modal) {
                    modal.classList.add('is-active');
                    document.body.style.overflow = 'hidden';
                }
            });
        });

        closers.forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                var modal = btn.closest('.ile-modal-backdrop');
                if (modal) {
                    modal.classList.remove('is-active');
                    document.body.style.overflow = '';
                }
            });
        });

        // Close on backdrop click & ESC key
        document.querySelectorAll('.ile-modal-backdrop').forEach(function (backdrop) {
            backdrop.addEventListener('click', function (e) {
                if (e.target === backdrop) {
                    backdrop.classList.remove('is-active');
                    document.body.style.overflow = '';
                }
            });
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                document.querySelectorAll('.ile-modal-backdrop.is-active').forEach(function (m) {
                    m.classList.remove('is-active');
                });
                document.body.style.overflow = '';
            }
        });
    }

    // Radio card style helper
    function updateRadioCardStyles(container) {
        container.querySelectorAll('.ile-radio-card').forEach(function (card) {
            var input = card.querySelector('input[type="radio"]');
            if (input && input.checked) {
                card.classList.add('selected');
            } else {
                card.classList.remove('selected');
            }
        });
    }

    // 5. Candidate Diagnostic Form Evaluation
    function initDiagnosticEvaluation() {
        var form = document.getElementById('ile-diagnostic-form');
        var submitBtn = document.getElementById('btn-submit-diagnostic');
        var resultBox = document.getElementById('ile-diagnostic-result');

        if (!form || !submitBtn || !resultBox) return;

        form.querySelectorAll('input[type="radio"]').forEach(function (r) {
            r.addEventListener('change', function () {
                updateRadioCardStyles(form);
            });
        });
        updateRadioCardStyles(form);

        var lang = (typeof window.ileData !== 'undefined' && window.ileData.currentLang) ? window.ileData.currentLang : 'it';

        var responses = {
            work: {
                it: {
                    title: "Orientamento: Ingresso per Lavoro Subordinato (Decreto Flussi / Formazione art. 23)",
                    summary: "Il tuo profilo è orientato all'inserimento lavorativo in Italia. I requisiti principali includono:",
                    docs: ["Contratto di soggiorno / Nulla Osta da parte dell'azienda italiana", "Passaporto in corso di validità", "Attestazione di idoneità professionale o linguistica prima della partenza", "Certificato carichi pendenti e casellario giudiziale legalizzato"],
                    advice: "Consigliato: completare il modulo di lingua italiana e cultura del lavoro su Italy Legal Entry per valorizzare la tua candidatura verso le aziende partner."
                },
                fr: {
                    title: "Orientation : Entrée pour Travail Salarié (Decreto Flussi / Formation art. 23)",
                    summary: "Votre profil est orienté vers l'insertion professionnelle en Italie. Les pièces principales requises sont :",
                    docs: ["Contrat de travail / Nulla Osta de l'employeur italien", "Passeport en cours de validité", "Attestation de formation linguistique/professionnelle avant départ", "Casier judiciaire légalisé et traduit"],
                    advice: "Recommandé : suivre le parcours préparatoire de langue italienne et de sécurité au travail sur la plateforme."
                },
                en: {
                    title: "Guidance: Entry for Employed Work (Quota Decree / Art. 23 Training)",
                    summary: "Your profile points to employed work opportunities in Italy. Key prerequisites include:",
                    docs: ["Employment contract / Work Clearance (Nulla Osta) from Italian employer", "Valid Passport", "Pre-departure linguistic and vocational training certificate", "Legalised police clearance record"],
                    advice: "Recommended: complete the Italian language and workplace culture modules on the platform."
                },
                ar: {
                    title: "التوجيه: مسار العمل المأجور (مرسوم التدفقات / التكوين بموجب المادة 23)",
                    summary: "ملفك مؤهل لمسار العمل في إيطاليا. المتطلبات الأساسية تشمل:",
                    docs: ["عقد عمل / ترخيص العمل (Nulla Osta) من المشغل الإيطالي", "جواز سفر ساري الصلاحية", "شهادة تكوين لغوي ومهني مسبق قبل السفر", "السجل العدلي / حسن السيرة مصادق عليه ومترجم"],
                    advice: "يُنصح بـ: استكمال وحدات اللغة الإيطالية وقواعد السلامة في العمل لتعزيز فرصك لدى الشركات الشريكة."
                }
            },
            family: {
                it: {
                    title: "Orientamento: Ricongiungimento Familiare (Art. 29 D.Lgs. 286/98)",
                    summary: "La procedura consente di raggiungere un familiare regolarmente soggiornante in Italia.",
                    docs: ["Nulla Osta per ricongiungimento rilasciato dallo Sportello Unico Immigrazione (SUI)", "Certificati di stato civile e parentela tradotti e legalizzati", "Certificato di idoneità alloggiativa e reddito minimo del richiedente in Italia", "Passaporto del familiare richiedente"],
                    advice: "Consigliato: verificare anticipatamente i limiti di reddito IRPEF aggiornati del familiare ospitante."
                },
                fr: {
                    title: "Orientation : Regroupement Familial (Art. 29 D.Lgs. 286/98)",
                    summary: "La procédure permet de rejoindre un proche résidant régulièrement en Italie.",
                    docs: ["Nulla Osta délivré par le Sportello Unico Immigrazione (SUI)", "Actes d'état civil et de filiation traduits et légalisés", "Attestation de logement conforme et justificatifs de ressources en Italie", "Passeport individuel en cours de validité"],
                    advice: "Recommandé : vérifier le barème de revenu minimum du membre de famille en Italie."
                },
                en: {
                    title: "Guidance: Family Reunification (Art. 29 D.Lgs. 286/98)",
                    summary: "This pathway allows you to join a family member legally residing in Italy.",
                    docs: ["Family Reunification Clearance (Nulla Osta) from the Immigration Desk (SUI)", "Certified and legalised civil status certificates", "Suitable housing certificate and minimum income proof in Italy", "Valid passport"],
                    advice: "Recommended: verify the required annual income thresholds of the sponsor in Italy."
                },
                ar: {
                    title: "التوجيه: مسار التجمع العائلي (المادة 29 من القانون 286/98)",
                    summary: "يتيح هذا الإجراء الالتحاق بأحد أفراد الأسرة المقيمين بصفة قانونية في إيطاليا.",
                    docs: ["ترخيص التجمع العائلي (Nulla Osta) الصادر عن مكتب الهجرة الموحد (SUI)", "عقود الحالة المدنية وإثباتات القرابة مترجمة ومصادق عليها", "شهادة مطابقة السكن وإثبات الدخل المالي للطرف المقيم بإيطاليا", "جواز سفر ساري المفعول"],
                    advice: "يُنصح بـ: التحقق من استيفاء شروط الدخل السنوي الأدنى المطلوب وملاءمة السكن."
                }
            },
            study: {
                it: {
                    title: "Orientamento: Visto per Studio / Iscrizione Universitaria (Universitaly)",
                    summary: "Percorso per corsi di laurea, master o formazione specialistica.",
                    docs: ["Preiscrizione confermata tramite portale Universitaly", "Dichiarazione di Valore / Attestato di Comparabilità CIMEA dei titoli scolastici", "Dimostrazione di mezzi economici di sussistenza per l'anno accademico", "Assicurazione sanitaria e alloggio"],
                    advice: "Consigliato: iniziare le pratiche di legalizzazione dei titoli di studio con largo anticipo."
                },
                fr: {
                    title: "Orientation : Visa d'Études / Inscription Universitaire (Universitaly)",
                    summary: "Procédure pour licence, master ou formation académique en Italie.",
                    docs: ["Préinscription validée sur la plateforme Universitaly", "Déclaration de valeur ou attestation de comparabilité CIMEA", "Justificatifs de moyens financiers de subsistance pour l'année", "Assurance médicale et logement"],
                    advice: "Recommandé : anticiper la traduction et légalisation de vos diplômes et relevés."
                },
                en: {
                    title: "Guidance: Student Visa / University Enrollment (Universitaly)",
                    summary: "Pathway for undergraduate, postgraduate, or vocational studies in Italy.",
                    docs: ["Confirmed pre-enrollment via the Universitaly portal", "Declaration of Value or CIMEA comparability statement", "Proof of sufficient financial subsistence for the academic year", "Health insurance and accommodation proof"],
                    advice: "Recommended: initiate diploma translations and legalisations well ahead of deadlines."
                },
                ar: {
                    title: "التوجيه: تأشيرة الدراسة / التسجيل الجامعي (Universitaly)",
                    summary: "مسار موجه للطلبة الراغبين في متابعة دراستهم الجامعية أو العليا بإيطاليا.",
                    docs: ["تأكيد التسجيل المسبق عبر منصة Universitaly الرسمية", "شهادة القيمة (Dichiarazione di Valore) أو إفادة المعادلة من CIMEA", "إثبات الموارد المالية الكافية لتغطية الموسم الجامعي", "التأمين الصحي وحجز السكن"],
                    advice: "يُنصح بـ: مباشرة إجراءات ترجمة وتصديق الشهادات وبيانات النقط مبكراً."
                }
            },
            visa: {
                it: {
                    title: "Orientamento: Visto di Breve Soggiorno Tipo C (Schengen)",
                    summary: "Soggiorno massimo di 90 giorni per turismo, visita privata o affari.",
                    docs: ["Modulo di domanda visto C debitamente compilato", "Prenotazione del volo andata/ritorno e alloggio confermato", "Lettera di invito (se per visita/affari) con garanzie economiche", "Fideiussione bancaria o estratti conto a garanzia dei mezzi economici"],
                    advice: "Nota: La decisione spetta esclusivamente al Consolato competente. Nessun esito garantito."
                },
                fr: {
                    title: "Orientation : Visa de Court Séjour Type C (Schengen)",
                    summary: "Séjour de 90 jours maximum pour tourisme, visite privée ou affaires.",
                    docs: ["Formulaire de visa C complété et signé", "Réservation de transport A/R et hébergement", "Lettre d'invitation (si visite privée/mission)", "Justificatifs de moyens financiers et assurance voyage"],
                    advice: "Note : La décision appartient exclusivement au Consulat. Aucun résultat n'est garanti."
                },
                en: {
                    title: "Guidance: Short-Stay Schengen Visa Type C",
                    summary: "Maximum 90-day stay for tourism, business, or private visit.",
                    docs: ["Duly completed Type C visa application form", "Round-trip travel reservation and confirmed lodging", "Invitation letter (if business/private visit)", "Proof of financial means and travel insurance"],
                    advice: "Note: Decision rests exclusively with the competent Consulate. No outcome is guaranteed."
                },
                ar: {
                    title: "التوجيه: تأشيرة الإقامة القصيرة نوع C (شنغن)",
                    summary: "إقامة لا تتجاوز 90 يوماً للسياحة أو الأعمال أو الزيارة الخاصة.",
                    docs: ["استمارة طلب التأشيرة معبأة وموقعة بدقة", "حجز تذكرة الطيران ذهاباً وإياباً وحجز الإقامة المؤكد", "خطاب الدعوة (في حالة الزيارة العائلية أو مهمة العمل)", "كشوفات الحساب البنكي كضمان مالي وتأمين السفر الدولي"],
                    advice: "ملاحظة هامة: القرار النهائي يعود حصرياً للقنصلية المختصة ولا وجود لنتائج مضمونة مسبقاً."
                }
            }
        };

        submitBtn.addEventListener('click', function () {
            var selectedGoal = form.querySelector('input[name="ile_goal"]:checked');
            var goalKey = selectedGoal ? selectedGoal.value : 'work';
            if (goalKey === 'degrees') goalKey = 'study'; // map foreign degrees to study/work pathway

            var data = responses[goalKey] ? responses[goalKey][lang] || responses[goalKey]['it'] : responses['work']['it'];

            var docsListHtml = data.docs.map(function (d) {
                return '<li>' + d + '</li>';
            }).join('');

            resultBox.innerHTML =
                '<h4 style="font-size:18px;margin-bottom:8px;color:var(--navy);font-weight:700;">' + data.title + '</h4>' +
                '<p style="font-size:14.5px;color:var(--grey);margin-bottom:12px;">' + data.summary + '</p>' +
                '<ul style="font-size:14px;margin-bottom:14px;padding-left:20px;line-height:1.5;">' + docsListHtml + '</ul>' +
                '<div style="font-size:13.5px;background:#fff;padding:12px;border:1px solid var(--rule);color:var(--navy);">' +
                '<strong>' + (lang === 'ar' ? 'توصية هامة: ' : 'Consiglio: ') + '</strong>' + data.advice +
                '</div>';

            resultBox.classList.add('show');
            resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });
    }

    // 6. Enterprise Form Submission
    function initEnterpriseForm() {
        var form = document.getElementById('ile-enterprise-form');
        var submitBtn = document.getElementById('btn-submit-enterprise');
        var resultBox = document.getElementById('ile-enterprise-result');

        if (!form || !submitBtn || !resultBox) return;

        var lang = (typeof window.ileData !== 'undefined' && window.ileData.currentLang) ? window.ileData.currentLang : 'it';

        var msgs = {
            it: "Grazie. La richiesta di contatto è stata registrata con successo. Il team di coordinamento AGAMI / Italy Legal Entry vi ricontatterà entro 48 ore lavorative.",
            fr: "Merci. Votre demande de contact a été enregistrée. L'équipe AGAMI / Italy Legal Entry prendra contact avec votre entreprise sous 48h ouvrées.",
            en: "Thank you. Your request has been registered. The AGAMI / Italy Legal Entry coordination team will reach out within 48 business hours.",
            ar: "شكراً لكم. تم تسجيل طلب التواصل الخاص بشركتكم بنجاح. سيتواصل معكم فريق التنسيق خلال 48 ساعة عمل."
        };

        submitBtn.addEventListener('click', function () {
            var name = form.querySelector('#ent_name').value.trim();
            var contact = form.querySelector('#ent_contact').value.trim();

            if (!name || !contact) {
                alert(lang === 'ar' ? 'يرجى إدخال اسم الشركة وبيانات التواصل' : 'Per favore compila tutti i campi obbligatori.');
                return;
            }

            resultBox.innerHTML = '<p style="color:var(--green);font-weight:600;margin:0;">' + (msgs[lang] || msgs['it']) + '</p>';
            resultBox.classList.add('show');
            form.reset();
        });
    }

    // 7. Persist language choice in Cookie
    function initLangCookieSync() {
        var langLinks = document.querySelectorAll('.lang a, .lang button');
        langLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                var lang = link.getAttribute('data-lang');
                if (lang) {
                    document.cookie = "ile_user_lang=" + lang + ";path=/;max-age=" + (60 * 60 * 24 * 365);
                }
            });
        });
    }

    // 8. Destinations Showcase Slider
    function initDestinationsSlider() {
        var track = document.getElementById('dest-slider-track');
        if (!track) return;

        var slides = track.querySelectorAll('.slide-card');
        if (!slides.length) return;

        var prevBtn = document.getElementById('slider-prev');
        var nextBtn = document.getElementById('slider-next');
        var currNumEl = document.getElementById('slider-curr-num');
        var playBtn = document.getElementById('slider-play-btn');
        var dots = document.querySelectorAll('.slider-dot');
        var viewport = document.getElementById('dest-slider-viewport');

        var currentIndex = 0;
        var totalSlides = slides.length;
        var autoplayInterval = 5000;
        var timer = null;
        var isPlaying = true;

        function updateSlide(index) {
            if (index < 0) index = totalSlides - 1;
            if (index >= totalSlides) index = 0;
            currentIndex = index;

            var isRtl = document.documentElement.getAttribute('dir') === 'rtl';
            var offset = currentIndex * 100;
            track.style.transform = isRtl ? 'translateX(' + offset + '%)' : 'translateX(-' + offset + '%)';

            slides.forEach(function (slide, i) {
                if (i === currentIndex) {
                    slide.classList.add('is-active');
                } else {
                    slide.classList.remove('is-active');
                }
            });

            if (currNumEl) {
                currNumEl.textContent = (currentIndex + 1 < 10 ? '0' : '') + (currentIndex + 1);
            }

            dots.forEach(function (dot, i) {
                if (i === currentIndex) {
                    dot.classList.add('is-active');
                    dot.setAttribute('aria-selected', 'true');
                    // Reset and restart CSS progress animation
                    var fill = dot.querySelector('.dot-progress-fill');
                    if (fill) {
                        fill.style.animation = 'none';
                        dot.offsetHeight; // trigger reflow
                        fill.style.animation = isPlaying ? 'dotProgressRun ' + (autoplayInterval / 1000) + 's linear forwards' : 'none';
                    }
                } else {
                    dot.classList.remove('is-active');
                    dot.setAttribute('aria-selected', 'false');
                    var oldFill = dot.querySelector('.dot-progress-fill');
                    if (oldFill) oldFill.style.animation = 'none';
                }
            });
        }

        function nextSlide() {
            updateSlide(currentIndex + 1);
        }

        function prevSlide() {
            updateSlide(currentIndex - 1);
        }

        function startAutoplay() {
            stopAutoplay();
            isPlaying = true;
            timer = setInterval(nextSlide, autoplayInterval);
            if (playBtn) {
                playBtn.innerHTML = '<span class="icon-pause">❚❚</span>';
                playBtn.setAttribute('aria-label', 'Pausa scorrimento');
            }
            var activeDot = document.querySelector('.slider-dot.is-active .dot-progress-fill');
            if (activeDot) {
                activeDot.style.animation = 'dotProgressRun ' + (autoplayInterval / 1000) + 's linear forwards';
            }
        }

        function stopAutoplay() {
            if (timer) {
                clearInterval(timer);
                timer = null;
            }
            isPlaying = false;
            if (playBtn) {
                playBtn.innerHTML = '<span class="icon-play">▶</span>';
                playBtn.setAttribute('aria-label', 'Riprendi scorrimento');
            }
            var activeDot = document.querySelector('.slider-dot.is-active .dot-progress-fill');
            if (activeDot) {
                activeDot.style.animationPlayState = 'paused';
            }
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', function () {
                nextSlide();
                if (isPlaying) startAutoplay();
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', function () {
                prevSlide();
                if (isPlaying) startAutoplay();
            });
        }

        if (playBtn) {
            playBtn.addEventListener('click', function () {
                if (isPlaying) {
                    stopAutoplay();
                } else {
                    startAutoplay();
                }
            });
        }

        dots.forEach(function (dot) {
            dot.addEventListener('click', function () {
                var targetIdx = parseInt(dot.getAttribute('data-slide-to'), 10);
                if (!isNaN(targetIdx)) {
                    updateSlide(targetIdx);
                    if (isPlaying) startAutoplay();
                }
            });
        });

        // Pause on hover
        if (viewport) {
            viewport.addEventListener('mouseenter', function () {
                if (isPlaying) {
                    clearInterval(timer);
                    var fill = document.querySelector('.slider-dot.is-active .dot-progress-fill');
                    if (fill) fill.style.animationPlayState = 'paused';
                }
            });

            viewport.addEventListener('mouseleave', function () {
                if (isPlaying) {
                    timer = setInterval(nextSlide, autoplayInterval);
                    var fill = document.querySelector('.slider-dot.is-active .dot-progress-fill');
                    if (fill) fill.style.animationPlayState = 'running';
                }
            });

            // Touch swipe
            var touchStartX = 0;
            var touchEndX = 0;

            viewport.addEventListener('touchstart', function (e) {
                touchStartX = e.changedTouches[0].screenX;
            }, { passive: true });

            viewport.addEventListener('touchend', function (e) {
                touchEndX = e.changedTouches[0].screenX;
                handleSwipe();
            }, { passive: true });

            function handleSwipe() {
                var threshold = 40;
                var isRtl = document.documentElement.getAttribute('dir') === 'rtl';
                var diff = touchStartX - touchEndX;

                if (Math.abs(diff) > threshold) {
                    if (diff > 0) {
                        isRtl ? prevSlide() : nextSlide();
                    } else {
                        isRtl ? nextSlide() : prevSlide();
                    }
                    if (isPlaying) startAutoplay();
                }
            }
        }

        // Initialize state & start autoplay
        updateSlide(0);
        startAutoplay();
    }

    // 9. Parcours Cards Slider (Without Images)
    function initParcoursSlider() {
        var track = document.getElementById('parcours-slider-track');
        if (!track) return;

        var slides = track.querySelectorAll('.parcours-slide');
        if (!slides.length) return;

        var prevBtn = document.getElementById('parcours-prev');
        var nextBtn = document.getElementById('parcours-next');
        var currNumEl = document.getElementById('parcours-curr-num');
        var dots = document.querySelectorAll('.parcours-dot');
        var viewport = document.getElementById('parcours-slider-viewport');

        var currentIndex = 0;
        var totalSlides = slides.length;

        function getVisibleCount() {
            var w = window.innerWidth;
            if (w <= 640) return 1;
            if (w <= 1020) return 2;
            return 3;
        }

        function updateParcours(index) {
            var visible = getVisibleCount();
            var maxIndex = Math.max(0, totalSlides - visible);

            if (index < 0) index = maxIndex;
            if (index > maxIndex) index = 0;
            currentIndex = index;

            var slideWidth = 100 / visible;
            var isRtl = document.documentElement.getAttribute('dir') === 'rtl';
            var offset = currentIndex * slideWidth;

            track.style.transform = isRtl ? 'translateX(' + offset + '%)' : 'translateX(-' + offset + '%)';

            slides.forEach(function (slide, i) {
                if (i >= currentIndex && i < currentIndex + visible) {
                    slide.classList.add('is-active');
                } else {
                    slide.classList.remove('is-active');
                }
            });

            if (currNumEl) {
                currNumEl.textContent = (currentIndex + 1 < 10 ? '0' : '') + (currentIndex + 1);
            }

            dots.forEach(function (dot, i) {
                if (i === currentIndex) {
                    dot.classList.add('is-active');
                    dot.setAttribute('aria-selected', 'true');
                } else {
                    dot.classList.remove('is-active');
                    dot.setAttribute('aria-selected', 'false');
                }
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', function () {
                updateParcours(currentIndex + 1);
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', function () {
                updateParcours(currentIndex - 1);
            });
        }

        dots.forEach(function (dot) {
            dot.addEventListener('click', function () {
                var targetIdx = parseInt(dot.getAttribute('data-parcours-to'), 10);
                if (!isNaN(targetIdx)) {
                    updateParcours(targetIdx);
                }
            });
        });

        // Touch swipe support
        if (viewport) {
            var touchStartX = 0;
            var touchEndX = 0;

            viewport.addEventListener('touchstart', function (e) {
                touchStartX = e.changedTouches[0].screenX;
            }, { passive: true });

            viewport.addEventListener('touchend', function (e) {
                touchEndX = e.changedTouches[0].screenX;
                var threshold = 35;
                var isRtl = document.documentElement.getAttribute('dir') === 'rtl';
                var diff = touchStartX - touchEndX;

                if (Math.abs(diff) > threshold) {
                    if (diff > 0) {
                        isRtl ? updateParcours(currentIndex - 1) : updateParcours(currentIndex + 1);
                    } else {
                        isRtl ? updateParcours(currentIndex + 1) : updateParcours(currentIndex - 1);
                    }
                }
            }, { passive: true });
        }

        // Window resize adjustment
        window.addEventListener('resize', function () {
            updateParcours(currentIndex);
        });

        updateParcours(0);
    }

    // Initialize all modules when DOM is ready
    document.addEventListener('DOMContentLoaded', function () {
        initRevealAnimations();
        initNavScroll();
        initMobileNav();
        initModals();
        initDiagnosticEvaluation();
        initEnterpriseForm();
        initLangCookieSync();
        initDestinationsSlider();
        initParcoursSlider();
    });

})();
