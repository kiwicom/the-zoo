const gitlabEnvs = {
 _fillData: (response) => {
    const envName = response['name'] || ""
    const envDashboardUrl = response['dashboardUrl'] || ""

    let $env = $('#env_template').clone()
    $env.find("input[name='gitlab-name']").val(envName)
    $env.find("input[name='gitlab-dashboard-url']").val(envDashboardUrl)
    $env.appendTo("#gitlab_envs" )
    $env.show()
  },
  load: (gitlabEnvsInfo) => {
    if (Number.isNaN(gitlabEnvsInfo.repoId)) { return }

    //delete previous gitlab envs
    $("#gitlab_envs").empty()
    //fetch gitlab envs
    $.get(gitlabEnvsInfo.envsUrl + "?project_id=" + gitlabEnvsInfo.repoId, function (response) {
      let customEnvsNameInput = $(".ui.segment.environment:visible").find(".field.name input")
      if (response.length == 0) {
        customEnvsNameInput.prop("required", true);
        return console.log('Fetching Gitlab environments completed! No envs.')
      }

      customEnvsNameInput.prop("required", false);
      $.each(response, function(index, element) {
        if (index > 10) { return;}
        gitlabEnvs._fillData(element)
      })
      console.log('Fetching Gitlab environments completed!')
    }).fail(function() {
      console.log( "Error fetching envs" );
    })
  }
}

export {gitlabEnvs};
