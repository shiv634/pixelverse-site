/* Pixelverse — shared behaviour: header, menu, video reels, lightbox, portfolio filter, contact form */
(function () {
  'use strict';

  /* ───────── settings you may edit ───────── */
  var PV = {
    email: 'pixelverse.va@gmail.com',
    // Paste a form endpoint here (for example a Formspree or Web3Forms URL) to send enquiries
    // straight to your inbox. While this is empty, the form opens the visitor's email app instead.
    formEndpoint: ''
  };

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ───────── header + menu ───────── */
  var header = $('.site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  var menuBtn = $('.menu-btn'), nav = $('#nav');
  function setMenu(open) {
    if (!menuBtn) return;
    document.body.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.firstChild.nodeValue = open ? 'Close' : 'Menu';
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () { setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'); });
    $$('#nav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    window.matchMedia('(min-width:761px)').addEventListener('change', function () { setMenu(false); });
  }

  /* ───────── reels ───────── */
  var WORK = window.PV_WORK || [];
  var byId = {}; WORK.forEach(function (w) { byId[w.id] = w; });
  var saveData = !!(navigator.connection && navigator.connection.saveData);
  var slowNet = !!(navigator.connection && /(^|-)(2g|3g)$/.test(navigator.connection.effectiveType || ''));
  var smallScreen = window.matchMedia('(max-width:760px)').matches;

  function buildReel(host) {
    var w = byId[host.getAttribute('data-reel')];
    if (!w) return;
    var b = document.createElement('button');
    b.className = 'reel'; b.type = 'button'; b.setAttribute('data-work', w.id);
    b.setAttribute('aria-label', 'Play the ' + w.title + ', ' + w.time);
    var layers = document.createElement('span'); layers.className = 'layers'; layers.setAttribute('aria-hidden', 'true');
    for (var i = 0; i < 3; i++) {
      var im = new Image(); im.alt = ''; im.decoding = 'async'; im.loading = 'lazy'; im.referrerPolicy = 'no-referrer';
      im.addEventListener('error', function () { b.classList.add('noposter'); });
      im.src = w.poster; layers.appendChild(im);
    }
    var pv = document.createElement('video');
    pv.className = 'preview'; pv.muted = true; pv.loop = true; pv.playsInline = true; pv.preload = 'none';
    pv.setAttribute('aria-hidden', 'true'); pv.tabIndex = -1;
    var badge = document.createElement('span'); badge.className = 'badge';
    badge.innerHTML = '<span class="dot"></span>' + w.label + '<span class="time">' + w.time + '</span>';
    var play = document.createElement('span'); play.className = 'play'; play.setAttribute('aria-hidden', 'true');
    b.appendChild(layers); b.appendChild(pv); b.appendChild(badge); b.appendChild(play);
    host.appendChild(b);

    // muted hover preview (mouse only, never on data saver)
    var timer = 0;
    if (!saveData) {
      b.addEventListener('pointerenter', function (e) {
        if (e.pointerType !== 'mouse') return;
        timer = setTimeout(function () {
          if (!pv.src) pv.src = w.src[360];
          var p = pv.play(); if (p && p.then) p.then(function () { b.classList.add('previewing'); }).catch(function () {});
        }, 260);
      });
      b.addEventListener('pointerleave', function () {
        clearTimeout(timer); b.classList.remove('previewing'); pv.pause();
      });
    }
    b.addEventListener('click', function () { clearTimeout(timer); pv.pause(); b.classList.remove('previewing'); openLightbox(w, b); });
  }
  $$('[data-reel]').forEach(buildReel);

  /* ───────── lightbox ───────── */
  var lb, lbVideo, lbTitle, lbMsg, lbOpener;
  function ensureLightbox() {
    if (lb) return;
    lb = document.createElement('dialog'); lb.className = 'lightbox'; lb.setAttribute('aria-labelledby', 'lb-title');
    lb.innerHTML =
      '<div class="lb-bar"><span class="lb-title" id="lb-title"></span><button class="btn lb-close" type="button">Close</button></div>' +
      '<div class="lb-frame"><video controls playsinline preload="metadata"></video><div class="lb-msg" role="alert"></div></div>';
    document.body.appendChild(lb);
    lbVideo = $('video', lb); lbTitle = $('.lb-title', lb); lbMsg = $('.lb-msg', lb);
    $('.lb-close', lb).addEventListener('click', function () { lb.close(); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener('close', function () {
      lbVideo.pause(); lbVideo.removeAttribute('src'); lbVideo.load(); lbMsg.classList.remove('show');
      if (lbOpener) lbOpener.focus();
    });
    lbVideo.addEventListener('error', function () {
      if (!lbVideo.getAttribute('src')) return;
      lbMsg.innerHTML = '<strong>This video could not load.</strong><span>Check your connection, or <a class="textlink" target="_blank" rel="noopener" href="' + lbVideo.getAttribute('src') + '">open the file directly</a>.</span>';
      lbMsg.classList.add('show');
    });
  }
  function openLightbox(w, opener) {
    ensureLightbox(); lbOpener = opener;
    var q = (smallScreen || saveData || slowNet) ? 480 : 720;
    lbTitle.textContent = w.title; lbMsg.classList.remove('show');
    lbVideo.src = w.src[q];
    lb.showModal();
    var p = lbVideo.play(); if (p && p.catch) p.catch(function () { /* controls stay available */ });
  }

  /* ───────── portfolio filters ───────── */
  var filters = $$('[data-filter]');
  if (filters.length) {
    var items = $$('.work-item'), invite = $('.invite');
    var apply = function (f, push) {
      var shown = 0;
      items.forEach(function (it) { var on = f === 'all' || it.getAttribute('data-id') === f; it.hidden = !on; it.classList.remove('single'); if (on) shown++; });
      if (f !== 'all') items.forEach(function (it) { if (!it.hidden) it.classList.add('single'); });
      if (invite) invite.hidden = f !== 'all';
      filters.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-filter') === f)); });
      if (push) history.replaceState(null, '', f === 'all' ? location.pathname : '#' + f);
    };
    filters.forEach(function (b) { b.addEventListener('click', function () { apply(b.getAttribute('data-filter'), true); }); });
    var h = (location.hash || '').replace('#', '');
    apply(byId[h] ? h : 'all', false);
    window.addEventListener('hashchange', function () { var k = (location.hash || '').replace('#', ''); apply(byId[k] ? k : 'all', false); });
  }

  /* ───────── contact form ───────── */
  var form = $('form.pv');
  if (form) {
    var status = $('.form-status', form);
    var fields = { name: $('#f-name'), email: $('#f-email'), message: $('#f-message') };
    var setErr = function (k, msg) {
      var el = fields[k], out = $('#err-' + k);
      el.setAttribute('aria-invalid', msg ? 'true' : 'false'); out.textContent = msg || '';
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      status.className = 'form-status'; status.textContent = '';
      var v = { name: fields.name.value.trim(), email: fields.email.value.trim(), message: fields.message.value.trim(), need: $('#f-need').value };
      var bad = false;
      if (!v.name) { setErr('name', 'Enter your name.'); bad = true; } else setErr('name', '');
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) { setErr('email', 'Enter an email address we can reply to.'); bad = true; } else setErr('email', '');
      if (!v.message) { setErr('message', 'Tell us a little about the project.'); bad = true; } else setErr('message', '');
      if (bad) { var first = form.querySelector('[aria-invalid="true"]'); if (first) first.focus(); return; }
      if ($('#f-company').value) return; // honeypot

      if (PV.formEndpoint) {
        var btn = $('button[type=submit]', form); btn.disabled = true; status.textContent = 'Sending…';
        fetch(PV.formEndpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(v) })
          .then(function (r) { if (!r.ok) throw new Error('bad'); status.className = 'form-status ok'; status.textContent = 'Sent. We’ll reply to ' + v.email + '.'; form.reset(); })
          .catch(function () { status.className = 'form-status bad'; status.innerHTML = 'That didn’t send. Email us at <a class="textlink" href="mailto:' + PV.email + '">' + PV.email + '</a> instead.'; })
          .then(function () { btn.disabled = false; });
      } else {
        var body = 'Name: ' + v.name + '\nEmail: ' + v.email + '\nProject type: ' + v.need + '\n\n' + v.message;
        window.location.href = 'mailto:' + PV.email + '?subject=' + encodeURIComponent('Project enquiry from ' + v.name) + '&body=' + encodeURIComponent(body);
        status.className = 'form-status ok';
        status.innerHTML = 'Your email app should open with the message ready to send. If it doesn’t, write to <a class="textlink" href="mailto:' + PV.email + '">' + PV.email + '</a>.';
      }
    });
  }
})();

/* prefill the contact form's subject from ?need=volsplat */
(function () {
  try {
    var q = new URLSearchParams(location.search).get('need'), sel = document.getElementById('f-need');
    if (!q || !sel) return;
    for (var i = 0; i < sel.options.length; i++) {
      if (sel.options[i].value.toLowerCase().indexOf(q.toLowerCase()) === 0) { sel.selectedIndex = i; break; }
    }
  } catch (e) {}
})();
