import '../style/style.less';
import jQuery from 'jquery/src/jquery';
import 'fomantic-ui-css/semantic.min.js';
import * as Snackbar from 'node-snackbar/dist/snackbar.min.js';

window.jQuery = jQuery;
window.$ = jQuery;
window.Snackbar = Snackbar;

window.showSnackbar = function (msg) {
  Snackbar.show({text: msg})
}

$('.user-actions').popup({
    transition: 'fade down',
    hoverable: true,
    variation: 'inverted',
    position: 'bottom right',
    on: 'click',
    hideOnScroll: false
})
