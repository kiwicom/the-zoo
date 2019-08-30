<template>
  <div class="menu transition visible" v-if="visible">
    <div
      class="item"
      v-for="(f, i) in filters"
      :index="i"
      :class="{'selected': i === cursor}"
      :type="f.type"
      :value="f.name"
      v-on:click="addFilter"
      v-on:mouseover="setCursor"
    >
      <i class="ui user icon" v-if="f.type === 'owner'"></i>
      <i class="ui bug icon" v-if="f.type === 'namespace'"></i>
      <i class="ui heartbeat icon" v-if="f.type === 'status'"></i>
      {{ f.name }}
    </div>
    <div class="message" v-if="count === 0">No results found.</div>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        cursor: 0
      }
    },
    props: ['visible'],
    computed: {
      filters () {
        this.cursor = 0
        return this.$store.getters.filteredFilters
      },
      count () {
        console.log(this.filters)
        return this.filters.length
      }
    },
    methods: {
      addFilter () {
        if(this.visible && this.count > 0) {
          const obj = this.filters[this.cursor]
          this.$store.commit('addAppliedFilter', {
            type: obj.type,
            name: obj.name
          })
          this.$store.commit('setFilteringTerm', '')
        }
      },
      setCursor (event) {
        if(this.visible)
          this.cursor = parseInt(event.target.getAttribute('index'))
      },
      goUp () {
        if(this.visible)
          this.cursor = Math.max(this.cursor - 1, 0)
      },
      goDown () {
        if(this.visible)
          this.cursor = Math.min(this.cursor + 1, this.filters.length - 1)
      },
    },
    created () {
      this.$parent.$on('select', this.addFilter)
      this.$parent.$on('decreaseCursor', this.goUp)
      this.$parent.$on('increaseCursor', this.goDown)
    }
  }
</script>
