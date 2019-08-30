<template>
  <div class="ui icon message">
    <div class="ui icon" data-tooltip="Issue description from metadata file" data-inverted="">
      <i class="circle info icon"></i>
    </div>
    <div class="content">
      <h5>{{ issue.title }}</h5>
      <p v-html="issueDescription"></p>
      <p class="ui circular label" :class="effortColor">effort:{{ issue.effort }}</p>
      <p class="ui circular label" :class="severityColor">severity:{{ issue.severity }}</p>
    </div>
  </div>
</template>

<script>
  import hljs from "highlight.js/lib";
  import snarkdown from "snarkdown";

  export default {
    props: ["issue", "name"],
    data () {
      return {
        issueDescription: snarkdown(this.issue.description),
      }
    },
    computed: {
      descriptionId () {
        var name = this.name.replace(":", "-")
        return `issue-description-${name}`
      },
      effortColor () {
        switch (this.issue.effort) {
          case "low":
            return "green"
          case "medium":
            return "yellow"
          case "high":
            return "red"
          default:
            return ""
        }
      },
      severityColor () {
        switch (this.issue.severity) {
          case "advice":
            return "green"
          case "warning":
            return "yellow"
          case "critical":
            return "red"
          default:
            return ""
        }
      }
    },
    mounted () {
      $(this.$el.querySelectorAll("pre, code")).each(
        function(index, block) {
          hljs.highlightBlock(block);
        }
      );
    },
  }
</script>
