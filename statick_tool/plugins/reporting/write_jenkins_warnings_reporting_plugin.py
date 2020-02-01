"""Write issue reports to a file."""
from __future__ import print_function

from deprecated import deprecated

import os

from statick_tool.reporting_plugin import ReportingPlugin


@deprecated(version="0.3.1", reason="Jenkins Warnings plugin has reached end-of-life")
class WriteJenkinsWarningsReportingPlugin(ReportingPlugin):
    """Writes Statick results to a file."""

    def get_name(self):
        """Return the plugin name."""
        return "write_jenkins_warnings"

    def report(self, package, issues, level):
        """
        Write the results to a Jenkins Warnings plugin compatible file.

        Args:
            package (:obj:`Package`): The Package object that was analyzed.
            issues (:obj:`dict` of :obj:`str` to :obj:`Issue`): The issues
                found by the Statick analysis, keyed by the tool that found
                them.
            level: (:obj:`str`): Name of the level used in the scan.
        """
        # Do not write report to file if no output directory is given.
        if not self.plugin_context.args.output_directory:
            return None, True

        # We _should_ be in output_dir already, but let's be safe about it.
        output_dir = os.path.join(self.plugin_context.args.output_directory,
                                  package.name + "-" + level)

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        if not os.path.isdir(output_dir):
            print("Unable to create output directory at {}!".format(
                output_dir))
            return None, False

        output_file = os.path.join(output_dir,
                                   package.name + "-" + level + ".statick")
        print("Writing output to {}".format(output_file))
        with open(output_file, "w") as out:
            for _, value in issues.items():
                for issue in value:
                    if issue.cert_reference:
                        line = "[{}][{}][{}:{}][{} ({})][{}]\n".format(issue.filename,
                                                                       issue.line_number,
                                                                       issue.tool,
                                                                       issue.issue_type,
                                                                       issue.message,
                                                                       issue.cert_reference,
                                                                       issue.severity)
                    else:
                        line = "[{}][{}][{}:{}][{}][{}]\n".format(issue.filename,
                                                                  issue.line_number,
                                                                  issue.tool,
                                                                  issue.issue_type,
                                                                  issue.message,
                                                                  issue.severity)
                    out.write(line)

        return None, True
