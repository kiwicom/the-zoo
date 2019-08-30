<template>
  <div class="project ui issue segment">
    <h3 class="ui header">
      <span>
        <a :href="project.url">{{ project.name }}</a>
        <small>
          ·
          <a
            :class="{disabled: !project.repository.url}"
            :href="project.repository.url"
            target="_blank"
          >{{ project.repository.owner }}/{{ project.repository.name }}</a>
        </small>
      </span>
      <div class="flex-horizontal tags-wrapper">
        <a
          class="ui circular label"
          :class="{yellow: project.type == 'service', green: project.type == 'library'}"
        >type:{{ project.type }}</a>
      </div>
    </h3>
    <div class="actions-wrapper">
      <button @click="selectIssue" class="ui transparent icon button">
        <i :class="checkIconClass"></i>
      </button>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["project", "issue_name"],
    computed: {
      selected() {
        return this.$store.getters.isSelected(
          this.issue_name,
          this.project.repository.id
        );
      },
      checkIconClass() {
        if (this.selected) {
          return "ui large check square icon";
        } else {
          return "ui large square outline icon";
        }
      }
    },
    methods: {
      selectIssue() {
        this.$store.commit(this.selected ? "unselectIssues" : "selectIssues", {
          name: this.issue_name,
          repos_ids: [this.project.repository.id]
        });
      }
    }
  };
</script>
