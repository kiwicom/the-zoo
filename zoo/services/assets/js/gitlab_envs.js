const gitlabEnvs = {
  _fillData: (imageUrl, data) => {
    const name = "name" in data ? data.name : ""
    const dashboardUrl = "dashboardUrl" in data ? data.dashboardUrl : ""

    return `<div class="ui secondary segment environment">
            <div class="ui top left attached label paddingless gitlab-img">
              <img src="${imageUrl}" alt="gitlab">
            </div>
            <div class="two fields">
              <div class="field name">
                <label>Name</label>
                <input type="text" value="${name}" readonly>
              </div>
              <div class="field dashboard-url">
                <label>Dashboard URL</label>
                <input type="text" value="${dashboardUrl}" readonly>
              </div>
            </div>
            <div class="field logs-url">
              <label>Logs URL</label>
              <input type="text" value="" readonly>
            </div>
            <div class="field service-urls">
              <label>Service URLs</label>
              <input type="text" value="" readonly>
            </div>
            <div class="field open_api_url">
              <label>OpenAPI URL</label>
              <input type="text" value="" readonly>
            </div>
          </div>`
  },
  load: (gitlabEnvsInfo) => {
    const gitlabEnvsSelector = $("#gitlab-envs")
    //fetch gitlab envs
    $.get(gitlabEnvsInfo.envsUrl + "?project_id=" + gitlabEnvsInfo.repoId, function (response) {
      if (response.length == 0) { return console.log('Fetching Gitlab environments completed!') }

      //delete previous gitlab envs
      gitlabEnvsSelector.empty()

      for (let i = 0; i < response.length; i++) {
        gitlabEnvsSelector.append(gitlabEnvs._fillData(gitlabEnvsInfo.imageUrl, response[i]))
      }

    }).fail(function() {
      console.log( "Error fetching envs" );
    })
  }
}

export {gitlabEnvs};
