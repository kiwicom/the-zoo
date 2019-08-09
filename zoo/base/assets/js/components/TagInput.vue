<template>
    <div>
        <div class="ui fluid dropdown selection multiple">
            <div class="default text" v-if="!value">Click on the tags that apply to your project</div>
            <a class="ui label transition visible" :data-value="tag" v-for="tag in selectedTags" :key="tag">
                {{ tag }}
                <i class="delete icon" @click="removeTag(tag)"></i>
            </a>
            <input type="hidden" :name="inputName" :value="value">
        </div>
        <div class="flex-horizontal tag-container">
            <a class="ui tag label" :data-value="tag" v-for="tag in availableTags" :key="tag" @click="selectedTags.push(tag)">
                {{ tag }}
            </a>
        </div>
    </div>
</template>

<style lang="less">
    .tag-container {
        padding: .5em;
        justify-content: flex-start;

        .ui.tag.label {
            margin-right: .5em;
            padding: .5em .75em .5em 1em;
            font-size: .85em;

            &::before {
                height: 1.25em;
                width: 1.25em;
            }
        }
    }
</style>

<script>
    import * as R from "ramda"

    export default {
        data () {
            return {
                selectedTags: tagInputInfo.initialValue ? R.split(',', tagInputInfo.initialValue) : [],
                inputName: tagInputInfo.name
            }
        },
        computed: {
            availableTags () {
                return R.difference(tagList, this.selectedTags)
            },
            value () {
                return this.selectedTags.join(',')
            }
        },
        methods: {
            removeTag (tag) {
                this.selectedTags = R.difference(this.selectedTags, [tag])
            }
        }
    }
</script>