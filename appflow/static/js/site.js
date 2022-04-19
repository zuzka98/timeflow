import {
    LayoutServerInfo,
    mountWithLayoutServer,
} from "https://esm.sh/idom-client-react@0.38.1";

const serverInfo = new LayoutServerInfo({
    host: document.location.hostname,
    port: document.location.port,
    path: "/_site",
    //query: queryParams.user.toString(),
    secure: document.location.protocol == "https:",
});

mountWithLayoutServer(
    document.getElementById("idom-app"),
    serverInfo
);