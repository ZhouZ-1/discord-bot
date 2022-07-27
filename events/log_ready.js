const { DBlog } = require("../lib/database/dblog");

module.exports = {
    name: "ready",
    once: true,
    execute(client) {
        const guilds = client.guilds.cache.map(guild => guild.id);
        const logDB = new DBlog();
        global.logDB = logDB;

        (async() => {
            await logDB.create_tables();
            for(let i = 0; i < guilds.length; i++) {

                let g = client.guilds.cache.get(guilds[i])
                let channels = g.channels.cache

                channels_arr = [...channels.values()]
                channels_filtered = channels_arr.filter((c) => (c.type === "GUILD_TEXT"))

                for(let m in channels_filtered){
                    //console.log(channels_filtered[m].id, channels_filtered[m].name);
                    logDB.channel_add(channels_filtered[m].id, channels_filtered[m].name, g.id)
                }
            }
        })();
    },
};