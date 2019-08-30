<template>
  <div class="ui issue segments">
    <div class="ui issue segment accordion">
      <h4 class="ui header title" :class="{active: projectsVisible}" @click="showProjects">
        <i class="dropdown icon"></i>{{ name }}
        <div class="sub header">
          <p class="ui circular label">{{ issue.count | pluralize('project', 'projects') }}</p>
        </div>
      </h4>
      <div class="actions-wrapper">
        <button @click="selectIssue" class="ui transparent icon button">
          <i :class="checkIconClass"></i>
        </button>
      </div>
    </div>
    <div v-if="projectsVisible" class="ui segment secondary description">
      <issue-description v-if="projectsVisible" :issue="issue" :name="name"></issue-description>
    </div>
    <div v-if="projectsVisible" class="ui secondary segment projects">
      <issue-project-list v-if="projectsVisible" :issue="issue" :name="name"></issue-project-list>
    </div>
  </div>
</template>

<script>
  import IssueProjectList from './IssueProjectList'
  import IssueDescription from './IssueDescription'
  import * as R from "ramda";


  const URI = require("urijs");

  export default {
    props: ["issue", "name"],
    data () {
      return {
        projectsVisible: false,
      };
    },
    computed: {
      selected () {
        return this.$store.getters.isSelectedIssue(this.name)
      },
      checkIconClass () {
        if (this.selected) {
          return "ui large check square icon";
        } else {
          return "ui large square outline icon";
        }
      }
    },
    methods: {
      showProjects () {
        this.projectsVisible = !this.projectsVisible
      },
      selectIssue () {
        this.$store.commit(
          this.selected ? "unselectIssues" : "selectIssues",
          {name: this.name}
        );
      },
    },
    components: {
      IssueProjectList,
      IssueDescription
    }
  };
</script>
