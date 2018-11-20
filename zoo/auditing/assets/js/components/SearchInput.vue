<template>
  <div :class="{'ui fluid multiple search selection icon dropdown': true, 'active visible': suggestionsVisible}">
    <div v-if="!isOnEditMode && filtersCount === 0" class="default text">
      Filter results
    </div>
    <filter-chip v-for="f in filters" :id="f.name" :key="f.name" :type="f.type"></filter-chip>
    <input
      tabindex="1"
      type="text"
      id="search-input"
      class="search"
      :style="{'width': this.inputWidth}"
      v-model="term"
      @focus="onFocus"
      @blur="onBlur"
      @keydown.up.prevent="decreaseCounter"
      @keydown.down.prevent="increaseCounter"
      @keydown.enter.prevent="doAction"
    >
    <i v-on:click="doAction" class="inverted circular filter link icon"></i>
    <search-suggestions :visible="suggestionsVisible"></search-suggestions>
  </div>
</template>

<script>
  import FilterChip from './FilterChip'
  import SearchSuggestions from './SearchSuggestions'

  export default {
    data () {
      return {
        isOnEditMode: false
      }
    },
    props: ['filtersCount', 'filters'],
    computed: {
      inputWidth () {
        return Math.max(2, this.term.length * 12) + 'px'
      },
      term: {
        get () {
          return this.$store.state.filteringTerm
        },
        set (val) {
          this.$store.commit('setFilteringTerm', val)
          this.counter = 0
        }
      },
      suggestionsVisible () {
        return this.$store.state.filteringTerm.length > 0
      }
    },
    methods: {
      increaseCounter () {
        this.$emit('increaseCursor')
      },
      decreaseCounter () {
        this.$emit('decreaseCursor')
      },
      doAction () {
        if(this.$store.state.filteringTerm)
          this.$emit('select')
        else
          this.$parent.$emit('applyFilters')
      },
      onFocus () {
        this.isOnEditMode = true
      },
      onBlur () {
        this.isOnEditMode = false
      },
    },
    components: {
      FilterChip,
      SearchSuggestions
    }
  }
</script>
