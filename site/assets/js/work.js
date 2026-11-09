/* Pixelverse — work configuration
   The three reels below are the videos already on the live Wix site (served from Wix's media CDN).
   To swap a reel later: change `vid` (video id) and `poster`, or point `src` at your own hosted MP4s.
   Each reel can list its own files under `src` (keys: 360, 480, 720, 1080). */

(function () {
  var VID = 'https://video.wixstatic.com/video/';
  var IMG = 'https://static.wixstatic.com/media/';
  function wix(id) {
    var o = {};
    [360, 480, 720, 1080].forEach(function (q) { o[q] = VID + id + '/' + q + 'p/mp4/file.mp4'; });
    return o;
  }
  window.PV_WORK = [
    {
      id: 'vfx', label: 'VFX', title: 'VFX reel', time: '0:56',
      blurb: 'Simulation, compositing and the shots that can’t be filmed.',
      src: wix('de04dd_a81232c22a3b41ba9052ec4780e3a9c1'),
      poster: IMG + 'de04dd_a81232c22a3b41ba9052ec4780e3a9c1f000.jpg'
    },
    {
      id: '3d', label: '3D', title: '3D reel', time: '1:55',
      blurb: 'Worlds modelled, lit and rendered from nothing.',
      src: wix('de04dd_ef410382361e4c9587432df89b80c66b'),
      poster: IMG + 'de04dd_ef410382361e4c9587432df89b80c66bf000.jpg'
    },
    {
      id: 'ai', label: 'AI', title: 'AI reel', time: '0:58',
      blurb: 'Generative imagery, directed like a shoot.',
      src: wix('de04dd_424c8c70da464ef4ae63686e9099e20e'),
      poster: IMG + 'de04dd_424c8c70da464ef4ae63686e9099e20ef000.jpg'
    }
  ];
})();
