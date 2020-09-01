<template>
  <div :class="inputClasses">
    <i :class="{magic: true, icon: true, hidden: !changeUndid}"></i>
    <div class="ui repo hint popup">
     <div class="flex-horizontal">
       <div>
          🐒  Hey there!
          <br>
          <span class="text">I think that the correct repo may be <span class="ui mini yellow label repo-name">{{ this.owner }}/{{ this.name }}</span></span>
        </div>
        <div class="compact tiny yellow circular ui button" @click="undoAutoHint">
          Undo
        </div>
     </div>
    </div>
    <input
      :class="{search: true, pushed: changeUndid}"
      type="text"
      id="visible_repository"
      v-model="enteredText"
      autocomplete="off"
      @focus="onFocus"
      @blur="onBlur"
      @keydown.up.prevent="decreaseCursor"
      @keydown.down.prevent="increaseCursor"
      @keydown.enter.prevent="doAction"
      :required="repoInputInfo.required"
    >
    <i class="dropdown icon"></i>
    <input type="hidden" :name="repoInputInfo.name" :id="repoInputInfo.id" :data-initial-value="repoInputInfo.initialValue" v-model="inputValue">
    <repo-input-suggestions :inputHasFocus="isOnEditMode" ref="suggestions"></repo-input-suggestions>
  </div>
</template>

<script>
import { match } from "ramda"
import RepoInputSuggestions from "./RepoInputSuggestions"
import $ from 'jquery/src/jquery'

function createPopup () {
  $('i.magic.icon').popup({
    transition: 'fade down',
    exclusive: true,
    hoverable: true,
    variation: 'inverted',
    popup: $('.repo.hint.popup')
  })
}

function popupAction (action) {
  $('i.magic.icon').popup(action)
}

export default {
  template: "#repo-input-text-field-markup",
  data () {
    return {
      isOnEditMode: false,
      repoInputInfo: repoInputInfo,
      owner: '',
      name: '',
      changeUndid: false
    }
  },
  computed: {
    inputClasses () {
      return {
        ui: true,
        fluid: true,
        search: true,
        selection: true,
        dropdown: true,
        active: this.isOnEditMode && this.enteredText.length > 0,
        visible: this.isOnEditMode && this.enteredText.length > 0
      }
    },
    currentRepoName () {
      return `${this.owner}/${this.name}`
    },
    enteredText: {
      get () {
        return this.$store.state.enteredText
      },
      set: function(val) {
        // Here I'm capturing the hostname, the user and the repo name even if right now
        // we only use the last two
        const regexMatch = match(
          /https?\:\/\/([^\/]+)?\/(.+)\/([^\/]+)\/?/,
          val
        )
        if (regexMatch.length)
          this.$store.commit(
            "setEnteredText",
            regexMatch[2] + "/" + regexMatch[3]
          )
        else this.$store.commit("setEnteredText", val)
      }
    },
    inputValue: {
      get () {
        return this.$store.state.inputValue
      }
    }
  },
  watch: {
    currentRepoName () {
      const thereIsValidText = this.owner && this.name && this.currentRepoName !== this.enteredText
      if(thereIsValidText) {
        const guessedRepo = this.$store.getters.getRepoId(this.currentRepoName.toLowerCase())
        if (guessedRepo.length > 0) {
          createPopup()
          this.enteredText = this.currentRepoName
          this.$store.commit(
            "selectSuggestion",
            guessedRepo[0].id
          );
          this.changeUndid = true
        }
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
    undoAutoHint () {
      if (this.repoInputInfo.initialValue) {
        this.setInitialValue()
      } else {
        this.enteredText = ''
        this.doAction()
      }
      popupAction('hide')
      this.changeUndid = false
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
  components: {
    RepoInputSuggestions
  },
  mounted () {
    this.setInitialValue()
    const context = this

    $('input[name="owner"]').on('keyup', function () {
      context.owner = $('input[name="owner"]').val()
    })
    $('input[name="name"]').on('keyup', function () {
      context.name = $('input[name="name"]').val()
    })
    context.owner = $('input[name="owner"]').val()
    context.name = $('input[name="name"]').val()
    createPopup()
  }
}
</script>
