$(document).ready(function() {
  const URI = require('urijs')
  const searchInput = $('.ui.search input')
  const enterKeyCode = 13
  const slashKeyCode = 47
  const currentUrl = URI(window.location.href)
  const currentQuery = URI.parseQuery(currentUrl.query()).q

  $(document).keypress(function(event) {
    if(event.which == slashKeyCode) {
      event.preventDefault();
      searchInput.focus()
      searchInput.selectionStart = searchInput.selectionEnd = searchInput.value.length
    }
  });

  searchInput.keypress((event) => {
    if(event.which === enterKeyCode) {
      let newUrl = currentUrl.pathname('search')
      newUrl.search("")

      if(searchInput.val())
        newUrl.addSearch(URI.parseQuery('?q=' + searchInput.val()))
      window.location.href = newUrl.toString()
    }
  })

  if(currentQuery) {
    searchInput.val(currentQuery)
  }

});
