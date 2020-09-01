<template>
  <div class="issue-list ui segment loading">
    <template v-for="[severity, issue_list] in groupedIssues">
      <div
        :class="['ui', 'block', 'header', `severity-${severity}`]"
        :key="severity"
      >{{ formatSeverityText(severity) }}</div>
      <issue-header v-for="[name, issue] in issue_list" :key="name" :issue="issue" :name="name"></issue-header>
    </template>
    <div v-if="selectedIssuesCount > 0" class="ui yellow inverted segment table-actions">
      <div class="flex-horizontal selected-info">
        <h5 class="ui tiny header">
          {{ selectedIssuesCount | pluralize('issue', 'issues') }},
          {{ selectedPatchesCount | pluralize('patch', 'patches') }}
        </h5>
        <div
          class="ui compact tiny red circular icon button"
          v-if="selectedIssuesCount > 0"
          @click="clearSelected"
        >
          <i class="cancel circle icon"></i>
        </div>
      </div>
      <div>
        <div class="ui compact brown vertical animated button" @click="openIssues">
          <div class="hidden content">
            <i class="gitlab icon"></i>
          </div>
          <div class="visible content">Create issues</div>
        </div>
        <div
          class="ui compact brown vertical animated button"
          @click="applyPatches"
          :class="{disabled: selectedPatchesCount == 0}"
        >
          <div class="hidden content">
            <i class="file alternate icon"></i>
          </div>
          <div class="visible content">Apply patches</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { groupBy, sortBy } from "ramda"
  import IssueHeader from "./IssueHeader";

  const actionModal = $(".ui.basic.modal");
  const actionModalText = actionModal.find("#action-modal-text");

  const bySeverity = groupBy(issue => {
    const data = issue[1];
    return data.severity;
  });

  const severityOrder = sortBy(category => {
    const key = category[0];
    switch (key) {
      case "critical":
        return 0;
      case "warning":
        return 1;
      case "advice":
        return 2;
    }

    return -1;
  });

  export default {
    computed: {
      issues () {
        return this.$store.state.data.issues;
      },
      groupedIssues () {
        var res = severityOrder(
          Object.entries(
            bySeverity(Object.entries(this.$store.state.data.issues))
          )
        );
        return res;
      },
      selectedPatchesCount () {
        return this.$store.getters.selectedPatchesCount;
      },
      selectedIssuesCount () {
        return this.$store.getters.selectedIssuesCount;
      }
    },
    components: {
      IssueHeader
    },
    methods: {
      formatSeverityText (originalText) {
        return `${originalText.charAt(0).toUpperCase()}${originalText.slice(
          1
        )} issues`;
      },
      clearSelected () {
        this.$store.commit("clearSelectedIssues");
      },
      openIssues () {
        const store = this.$store;
        const issueCountText = pluralize(this.selectedIssuesCount, "issue", "issues");
        actionModal
          .modal({
            transition: "fade up",
            onShow () {
              actionModalText.html(
                `You are going to create ${issueCountText}, is this action intended?`
              );
            },
            onApprove () {
              const request = new XMLHttpRequest();
              request.onreadystatechange = function() {
                if (request.readyState === XMLHttpRequest.DONE) {
                  if (request.status === 200) {
                    const responseData = request.response;
                    store.commit("clearSelectedIssues");
                    store.commit("setAppData", responseData);
                    store.commit("initFilters");
                    showSnackbar("Issues created succesfully");
                  } else {
                    showSnackbar("Error creating issues. Please reload");
                  }
                }
              };
              request.open("POST", auditOverviewIssueEndpoint);
              request.setRequestHeader("X-CSRFToken", auditOverviewCsrfToken);
              request.responseType = "json";
              const requestData = JSON.stringify({
                selectedIssues: store.state.selectedIssues,
                filters: store.state.data.filters
              });
              request.send(requestData);
            }
          })
          .modal("show");
      },
      applyPatches () {
        const store = this.$store;
        const patchCountText = pluralize(this.selectedPatchesCount, "patch", "patches");
        actionModal
          .modal({
            transition: "fade up",
            onShow () {
              actionModalText.html(
                `You are going to apply ${patchCountText}, is this action intended?`
              );
            },
            onApprove () {
              const request = new XMLHttpRequest();
              request.onreadystatechange = function() {
                if (request.readyState === XMLHttpRequest.DONE) {
                  if (request.status === 200) {
                    const responseData = request.response;
                    store.commit("clearSelectedIssues");
                    store.commit("setAppData", responseData);
                    store.commit("initFilters");
                    showSnackbar("Patches applied succesfully");
                  } else {
                    showSnackbar("Error applying patches. Please reload");
                  }
                }
              };
              request.open("POST", auditOverviewPatchEndpoint);
              request.setRequestHeader("X-CSRFToken", auditOverviewCsrfToken);
              request.responseType = "json";
              const requestData = JSON.stringify({
                selectedIssues: store.state.selectedIssues,
                filters: store.state.data.filters
              });
              request.send(requestData);
            }
          })
          .modal("show");
      }
    }
  };
</script>
