# netdata-debsecan

Check/graph the number [CVE](https://en.wikipedia.org/wiki/Common_Vulnerabilities_and_Exposures)s in currently installed packages.

![](https://i.imgur.com/OIu846o.png)

This is a `python.d` module for [netdata](https://my-netdata.io/). It parses output from [debsecan](https://manpages.debian.org/stretch/debsecan/debsecan.1.en.html)

The number of vulnerabilities is graphed by scope (locally/remotely exploitable) and urgency (low/medium/high).



## Installation

This module expects the output of debsecan, split by scope/urgency in files at `/var/log/debsecan`. A [script](usr_local_bin_debsecan-by-type) to generate the expected reports is provided.

```bash
# install debsecan
apt install debsecan

# clone the repository
git clone https://gitlab.com/nodiscc/netdata-debsecan

# install the generation script
cp netdata-debsecan/usr_local_bin_debsecan-by-type /usr/local/bin/debsecan-by-type

# generate initial debsecan reports in /var/log/debsecan/
/usr/local/bin/debsecan-by-type

# (optional) configure dpkg to refresh the file after each run
# generating reports after each apt/dpkg run can take some time
cp netdata-debsecan/etc_apt_apt.conf.d_99debsecan /etc/apt/apt.conf.d/99debsecan

# add a cron job to refresh the file every hour
cp netdata-debsecan/etc_cron.d_debsecan /etc/cron.d/debsecan

# install the module/configuration file
netdata_install_prefix="/opt/netdata" # if netdata is installed from binary/.run script
netdata_install_prefix="" # if netdata is installed from OS packages
cp netdata-debsecan/debsecan.chart.py $netdata_install_prefix/usr/libexec/netdata/python.d/
cp netdata-debsecan/debsecan.conf $netdata_install_prefix/etc/netdata/python.d/

# restart netdata
systemctl restart netdata

```

You can also install this module using the [`nodiscc.xsrv.monitoring` ansible role](https://gitlab.com/nodiscc/xsrv/-/tree/master/roles/monitoring).


## Configuration

No configuration is required. Common `python.d` plugin options can be changed in [`debsecan.conf`](debsecan.conf).

The default `update every` value is 600 seconds so the initial chart will only be created after 10 minutes. Change this value if you need more accuracy.

You can get details on vulnerabilities by reading mail sent by debsecan, or by reading the output of `debsecan --format report`.

You can work towards decreasing the count of vulnerabilities by upgrading/patching/removing affected software, or by mitigating them through other means and adding them to debsecan's whitelist.

## Debug

To debug this module:

```bash
$ sudo su -s /bin/bash netdata
$ $netdata_install_prefix/usr/libexec/netdata/plugins.d/python.d.plugin 1  debug trace debsecan
```

## TODO

- Document alarm when total number of CVEs changes
- Document alarm when number of remote/high CVEs is above a threshold
- Configure debsecan to generate the status file after each APT run (see `/etc/debsecan/notify.d/600-mail`)

## License

[GNU GPLv3](LICENSE)

## Mirrors

- https://github.com/nodiscc/netdata-debsecan
- https://gitlab.com/nodiscc/netdata-debsecan

