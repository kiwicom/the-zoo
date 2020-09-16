<template>
  <div class="menu transition visible"
    v-if="visible"
    @keydown.up="increaseCounter"
    @mouseover="setCursor"
    @mouseleave="resetCursor"
  >
    <div
      :index="i" :key="i"
      v-for="(suggestion, i) in visibleSuggestions"
      :class="{'selected': i === cursor, 'item': true}"
    >
      <span v-html="suggestion.label"></span>
    </div>
    <div class="item" style="text-align: center;" v-if="count === 0">
    <span>
        No results found
    </span>
    </div>
  </div>
</template>

<script>
import { take } from "ramda"

export default {
  template: "#repo-input-suggestions-markup",
  props: ["inputHasFocus"],
  data () {
    return {
      cursor: -1,
      cursorMax: 0,
    };
  },
  watch: {
    suggestions () {
      this.cursor = -1;
    },
  },
  computed: {
    showCount () {
      if (this.cursor > this.cursorMax) {
        this.cursorMax = this.cursor;
      }
      return this.cursorMax + 10;
    },
    suggestions () {
      return this.$store.getters.getFilteredSuggestions;
    },
    visibleSuggestions () {
      return take(this.showCount, this.suggestions);
    },
    count () {
      return this.suggestions.length;
    },
    visible () {
      return this.inputHasFocus;
    },
  },
  methods: {
    selectSuggestion () {
      if (this.visible && this.count > 0 && this.cursor >= 0) {
        this.$store.commit(
          "selectSuggestion",
          this.suggestions[this.cursor].id,
        );
      } else if (this.$store.state.enteredText === "") {
        console.log(this.cursor);
        this.$store.commit(
          "selectSuggestion",
          "",
        );
      }
    },
    blurActiveElement () {
      document.activeElement.blur();
    },
    setCursor: function(event) {
      if (this.visible) {
        if (event.target.hasAttribute("index")) {
          var element = event.target;
        } else if (event.target.closest("div.selected")) {
          var element = event.target.closest("div.selected");
        }
        if (element !== undefined) {
          this.cursor = parseInt(element.getAttribute("index"));
        }
      }
    },
    resetCursor () {
      this.cursor = -1;
    },
    goUp () {
      if (this.visible) this.cursor = Math.max(this.cursor - 1, 0);
    },
    goDown () {
      if (this.visible)
        this.cursor = Math.min(this.cursor + 1, this.suggestions.length - 1);
    },
  },
  created () {
    this.$parent.$on("select", this.blurActiveElement);
    this.$parent.$on("decreaseCursor", this.goUp);
    this.$parent.$on("increaseCursor", this.goDown);
  }
};
</script>
