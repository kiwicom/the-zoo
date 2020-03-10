import 'jquery-tablesort/jquery.tablesort.min.js'


$(document).ready(() => {
  // For the Internal/Public switcher
  $(".ui.dropdown").dropdown();

  // Make the data table sortable

  $(".ui.table").tablesort();
});
