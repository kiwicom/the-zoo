<template>
    <div class="menu transition visible"
        v-if="visible"
        @keydown.up="increaseCounter"
        v-on:click="selectSuggestion"
        @mouseover="setCursor"
    >
        <div :index="i" v-for="(suggestion, i) in suggestions" :key="suggestion.reference" :class="{'selected': i === cursor, 'item': true}">
        <span>{{ suggestion.reference }} </span>
        </div>
        <div class="item" style="text-align: center;" v-if="count === 0">
        <span>
            No results found
        </span>
        </div>
    </ul>
  </div>
</template>

<script>
export default {
  data () {
    return {
      cursor: 0
    };
  },
  template: "#repo-input-suggestions-markup",
  props: ["inputHasFocus"],
  computed: {
    suggestions () {
      this.cursor = 0;
      return this.$store.getters.getFilteredSuggestions;
    },
    count () {
      return this.suggestions.length;
    },
    visible () {
      return this.$store.state.enteredText.length > 0 && this.inputHasFocus;
    }
  },
  methods: {
    selectSuggestion () {
      if (this.visible) {
        this.$store.commit(
          "selectSuggestion",
          this.suggestions[this.cursor].id
        );
        document.activeElement.blur();
      }
    },
    setCursor: function(event) {
      if (this.visible)
        this.cursor = parseInt(event.target.getAttribute("index"));
    },
    goUp () {
      if (this.visible) this.cursor = Math.max(this.cursor - 1, 0);
    },
    goDown () {
      if (this.visible)
        this.cursor = Math.min(this.cursor + 1, this.suggestions.length - 1);
    }
  },
  created () {
    this.$parent.$on("select", this.selectSuggestion);
    this.$parent.$on("decreaseCursor", this.goUp);
    this.$parent.$on("increaseCursor", this.goDown);
  }
};
</script>
