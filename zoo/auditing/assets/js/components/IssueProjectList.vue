<template>
  <div class="ui segments">
    <project-header
      v-for="(project, index) in pageProjects"
      :key="index"
      :project="project"
      :issue_name="name"
    ></project-header>
    <div v-if="numberOfPages > 1" class="ui secondary center aligned segment">
      <div class="ui pagination menu">
        <a @click="prevPage" class="item" :class="{disabled: page < 2}">
          <i class="chevron left icon"></i>
        </a>
        <div class="item">Page {{ page }} of {{ numberOfPages }}</div>
        <a @click="nextPage" class="item" :class="{disabled: page >= numberOfPages}">
          <i class="chevron right icon"></i>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
  import ProjectHeader from "./ProjectHeader"
  import { curry, isEmpty, prepend, take, drop } from "ramda"

  var groupsOf = curry(function group(n, list) {
    return isEmpty(list)
      ? []
      : prepend(take(n, list), group(n, drop(n, list)))
  })

  export default {
    props: ["issue", "name"],
    data() {
      return {
        page: 1
      }
    },
    computed: {
      projectsGroups () {
        return groupsOf(10, this.issue.projects)
      },
      numberOfPages () {
        return this.projectsGroups.length
      },
      pageProjects () {
        return this.projectsGroups[this.page - 1]
      }
    },
    methods: {
      nextPage () {
        if (this.page < this.numberOfPages) {
          this.page++
        }
      },
      prevPage () {
        if (this.page > 1) {
          this.page--
        }
      }
    },
    components: {
      ProjectHeader
    }
  }
</script>
