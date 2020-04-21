<template>
  <div class="ui search item">
    SOMETHING
    <div class="ui icon input">
      <input id="searchbox" name="q" type="text" value="{{ request.GET.q }}" placeholder="Search..."/>
      <i class="search icon"></i>
    </div>
  </div>
</template>

<script>
import * as R from "ramda"
import $ from 'jquery/src/jquery'

export default {
  data () {
    return {
      repoInputInfo: {},
      isOnEditMode: false,
    }
  },
  computed: {
    inputClasses () {
      return {
        ui: true,
        search: true,
        selection: true,
        dropdown: true,
        active: this.isOnEditMode && this.enteredText.length > 0,
        visible: this.isOnEditMode && this.enteredText.length > 0
      }
    },
    enteredText: {
      get () {
        return this.$store.state.enteredText
      },
      set: function(val) {
        this.$store.commit("setEnteredText", val)
      }
    },
    inputValue: {
      get () {
        return this.$store.state.inputValue
      }
    }
  },
  methods: {
    increaseCursor () {
      this.$emit("increaseCursor")
    },
    decreaseCursor () {
      this.$emit("decreaseCursor")
    },
    doAction () {
      this.$emit("select")
    },
    onFocus () {
      this.isOnEditMode = true
    },
    setInitialValue () {
      if (this.repoInputInfo.initialValue) {
        this.$store.commit("selectSuggestion", parseInt(this.repoInputInfo.initialValue))
        this.$store.commit("refreshEnteredText")
      }
    },
    onBlur () {
      this.$refs.suggestions.selectSuggestion();
      this.isOnEditMode = false
      this.$store.commit("refreshEnteredText")
    },
  },
}
</script>
