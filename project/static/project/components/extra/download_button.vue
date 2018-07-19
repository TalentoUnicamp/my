<template>
    <sui-dropdown
    class="icon blue scrolling"
    icon="download"
    button
    fluid
    labeled
    text="Download">
    <sui-dropdown-menu>
        <div class="header">
            <i class="file alternate icon"></i>
            Formatos disponíveis
        </div>
        <sui-dropdown-item @click="downloadAs('csv')">
            <div class="ui red empty circular label" />
            CSV
        </sui-dropdown-item>
        <sui-dropdown-item @click="downloadAs('csv2')">
            <div class="ui blue empty circular label" />
            CSV sem prefixo
        </sui-dropdown-item>
        <sui-dropdown-item @click="downloadAs('tsv')">
            <div class="ui green empty circular label" />
            TSV
        </sui-dropdown-item>
        <sui-dropdown-item @click="downloadAs('tsv2')">
            <div class="ui yellow empty circular label" />
            TSV sem prefixo
        </sui-dropdown-item>
        <sui-dropdown-item @click="downloadAs('json')">
            <div class="ui brown empty circular label" />
            JSON
        </sui-dropdown-item>
        <sui-dropdown-item @click="downloadAs('xml')">
            <div class="ui teal empty circular label" />
            XML
        </sui-dropdown-item>
        <sui-dropdown-item @click="downloadAs('yaml')">
            <div class="ui orange empty circular label" />
            YAML
        </sui-dropdown-item>
        <sui-dropdown-item @click="downloadAs('msgpack')">
            <div class="ui pink empty circular label" />
            MessagePack
        </sui-dropdown-item>
    </sui-dropdown-menu>
</sui-dropdown>
</template>

<script>
export default {
    props: ["url"],
    methods: {
        downloadAs(format) {
            window.location.href = this.url + "?format=" + format;
        }
    }
};
</script>
