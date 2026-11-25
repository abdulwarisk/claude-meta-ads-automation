# Setting up Claude Code with Meta's Ads server

Server URL: `https://mcp.facebook.com/ads`

## Option 1: no Meta app (try this first)
```bash
claude mcp add --transport http --scope user meta-ads https://mcp.facebook.com/ads
```
In Claude Code, run `/mcp` → **meta-ads** → **Authenticate**, log in with Facebook, approve, and pick your ad account.

## Option 2: with your own Meta app (if Option 1's login fails)
Some people see `redirect_uris are not registered for this client` with Option 1. If that happens:
1. Go to developers.facebook.com/apps and create an app (or open one you already have).
2. Add the use case **"Create & manage ads with ads MCP server"**.
3. In **Facebook Login for Business** settings, add the redirect URL Claude Code shows during login.
4. Remove the old entry and add it again with your App ID:
```bash
claude mcp remove meta-ads
claude mcp add --transport http --scope user --client-id <META_APP_ID> meta-ads https://mcp.facebook.com/ads
```
5. Run `/mcp` → **meta-ads** → **Authenticate** again.

## Check it works
Ask Claude: `Using meta-ads, list my ad accounts and their currency. Read only.`

## Common problems
- **Tools not showing:** restart Claude Code after `claude mcp add`, then run `/mcp`.
- **No ad accounts listed:** your Facebook profile needs access to the ad account in Business settings.
- **Permission error when creating:** check the Ads MCP server permissions in Business Suite (see `safety-business-suite.md`).
