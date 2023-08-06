# FAST-MPF

FAST-MPF is a fork of the open source [Mission Pinball Framework](https://missionpinball.org)
(MPF) project optimized for use with FAST Pinball hardware. It's MIT-licensed,
open source, and available for free, (though commercial suppport is available
from FAST Pinball). FAST-MPF is maintained by Brian Madden,
brian@fastpinball.com.

FAST-MPF is being streamlined and customized for FAST Pinball hardwware,
and will include several structural changes under the hood to align MPF's
hardware interface to FAST Pinball's hardware. It largely maintains compatibility with MPF, though configuration sections related to hardware devices are being significantly restructured, and several new config sections
are being added.

FAST-MPF is a fork of the core MPF repo only, (since it's the only part of
the larger MPF ecosystem which directly interfaces with hardware). Users of FAST-MPF can still use the other open source MPF projects, such as the MPF
Media Controller (MPF-MC), MPF Monitor, and Showcreator.

Bug fixes and enhancements to made to FAST-MPF that do not directly involve
FAST Pinball hardware will be submitted back to the open source MPF project,
and we expect to pull in non-hardware-related changes from the open source
MPF into FAST-MPF as well.

We will also continue to support, maintain, and improve the other open source
MPF modules.
## License

FAST-MPF is released under the MIT License. (This is the same license as the
original MPF project it was forked from.) You are free to use it how you wish,
but it only works with FAST Pinball hardware.
