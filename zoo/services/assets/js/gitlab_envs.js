const gitlabEnvs = {
  _resetGilabEnvs: (envTypeGitlab) => {
    const gitlab_envs = $("input[value='" + envTypeGitlab + "']").closest(".ui.segment");
    if (gitlab_envs.length > 0) {
      $.each(gitlab_envs, function(index, element){
        const uiSegment = $(element)

        // set values to default
        uiSegment.find(".field.name input").val("");
        uiSegment.find('input[name$="type"]').val("");
        uiSegment.find('input[name$="dashboard_url"]').val("");
        uiSegment.find('input[name$="logs_url"]').val("");
        uiSegment.find('input[name$="open_api_url"]').val("");
        uiSegment.find('input[name$="logs_url"]').val("");
        uiSegment.find('input[name$="logs_url"]').val("");

        // remove gitlab icon
        uiSegment.find(".gitlab-img").hide()

        $('input[id*="open_api_url_"]').each(function(index, element){
          element.val("")
          if (index != 0) {
            element.hide();
          }
        })

        uiSegment.hide();
        uiSegment.find(".field.name input").prop("required", false);

        //if all segments are hidden,
        const hidden = $(".ui.segment.environment:hidden");
        if (hidden.length == 5) {
          let firstSegment = hidden.eq(0);
          firstSegment.show()
        }

        if (hidden.length > 0) {
            $("button.add-environment").prop("disabled", false);
        }

      })
    }
  },
  _getFirstAvailableSegment: () => {
    const all_envs = $(".ui.segment.environment");
    if (all_envs.length == 0) {
      return false;
    }

    for (let i = 0; i < all_envs.length; i++) {
      let firstSegment = all_envs.eq(i)
      if (firstSegment.find(".field.name input").val() == "") {
          return firstSegment
      }
    }

    return false;
  },
  _fillData: (envTypeGitlab, firstSegment, response) => {
    firstSegment.find(":not(.no-reset) input").val("");
    firstSegment.find(".field.name input").val(response["name"]);
    firstSegment.find('input[name$="type"]').val(envTypeGitlab);
    firstSegment.find('input[name$="dashboard_url"]').val(response["dashboardUrl"]);
    firstSegment.find('input[name$="logs_url"]').val(response["logsUrl"]);
    firstSegment.find('input[name$="open_api_url"]').val(response["openApiUrl"]);

    for (let j = 0; j < response["serviceUrl"].length; j++) {
      if (j > 4) {
        break;
      }

      let selector = `input[id$="open_api_url_${j}"]`
      let el = firstSegment.find(selector)
      el.val(response["openApiUrl"][0]);
      el.show();
    }
    firstSegment.find(".gitlab-img").show()
    firstSegment.show();
  },
  load: (gitlabEnvsInfo) => {
    //delete previous gitlab envs
    gitlabEnvs._resetGilabEnvs(gitlabEnvsInfo.envTypeGitlab)

    //fetch gitlab envs
    $.get(gitlabEnvsInfo.envsUrl + "?project_id=" + gitlabEnvsInfo.repoId, function (response) {
      const arrayLength = response.length;

      if (arrayLength == 0) {
        return alert('Fetching Gitlab enviroments completed!')
      }

      for (let i = 0; i < arrayLength; i++) {
        let firstSegment = gitlabEnvs._getFirstAvailableSegment();
        if (!firstSegment) { break;}
        gitlabEnvs._fillData(gitlabEnvsInfo.envTypeGitlab, firstSegment, response[i])

        const hidden = $(".ui.segment.environment:hidden");

        if (hidden.length == 0) {
          $("button.add-environment").prop("disabled", true);
        }
      }

    }).fail(function() {
      console.log( "Error fetching envs" );
    })
  }
}

export {gitlabEnvs};
