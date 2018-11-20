<template>
  <a class="ui label transition visible" style="display: inline-block !important;">
    <i :class="icon + ' icon'"></i>
    {{ id }}
    <i v-on:click="selfRemove" class="delete icon"></i>
  </a>
</template>

<script>
  export default {
    name: 'filter-chip',
    props: ['id', 'type'],
    computed: {
      icon () {
        switch(this.type) {
          case 'owner': return 'user'
          case 'namespace': return 'bug'
          case 'status': return 'heartbeat'
        }
        return 'question'
      }
    },
    methods: {
      selfRemove () {
        this.$store.commit('removeAppliedFilter', {
          'name': this.id,
          'type': this.type
        })
      }
    }
  }
</script>
