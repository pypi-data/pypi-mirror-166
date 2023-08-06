import argparse
import ast
import fnmatch
import glob
import os
import re
from typing import Dict, List


class ParsingError(Exception):
    """
    Unable to parse this Dockerfile, are you sure it is valid syntax?
    """
    def __str__(self):
        return self.__doc__


class DockerfileParser:
    def __init__(self, dockerfile: str = None, raw_text: str = None, dockerignore: str = ".dockerignore"):
        self.valid_instructions = ["#", "COMMENT", "FROM", "COPY", "ADD", "WORKDIR", "EXPOSE", "USER", "ARG", "ENV",
                                   "LABEL", "RUN", "CMD", "ENTRYPOINT", "ONBUILD", "HEALTHCHECK", "STOPSIGNAL",
                                   "VOLUME", "SHELL", "MAINTAINER"]
        if dockerfile is not None:
            self.df_content = self._read_file(path=dockerfile)
        elif raw_text is not None:
            self.df_content = raw_text.splitlines()
        else:
            raise TypeError("Neither a Dockerfile path nor raw text input were provided")

        self.docker_ignore_files = self._read_file(path=dockerignore, docker_ignore=True)
        self.df_ast = self.parse_dockerfile()

    @staticmethod
    def _read_file(path: str, docker_ignore: bool = False) -> List:
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = f.read().splitlines()
            return data
        else:
            if docker_ignore:
                return []
            raise FileNotFoundError(f"Dockerfile not found, path: {path}")

    def _get_state(self, line: str) -> str:
        line = line.rstrip()
        if line == "":
            state = "blank"
        elif line.strip().startswith("#"):
            state = "comment"
        elif line.split(" ", 1)[0] in self.valid_instructions and line.endswith("\\"):
            state = "new_multi_line_command"
        elif line.endswith("\\"):
            state = "continued_multi_line_command"
        elif not line.endswith("\\") and line.split(" ", 1)[0] not in self.valid_instructions:
            state = "end_multi_line_command"
        else:
            state = "new_command"
        return state

    @staticmethod
    def _get_instruction(line: str) -> [str, None]:
        if line != "":
            if line.strip().startswith("#"):
                instruction = "COMMENT"
            else:
                instruction = line.split(" ", 1)[0]
            return instruction
        return None

    def _get_raw_command(self, line: str) -> [str, None]:
        if line.startswith("#"):
            return line.split("#", 1)[1].replace("#", "")
        elif line == "":
            return None
        elif line.split(" ", 1)[0] in self.valid_instructions:
            return line.split(" ", 1)[1].strip()
        else:
            return line.strip()

    @staticmethod
    def _parse_json_notation(command: str) -> dict:
        out = dict(executable=None, arguments=[])
        try:
            run_eval = ast.literal_eval(command)
        except (SyntaxError, ValueError):
            run_eval = command
        if isinstance(run_eval, list):
            if len(run_eval) == 0:
                out["arguments"] = run_eval[1:]
                return out
            if run_eval[0].startswith("--"):
                out["docker_syntax"] = run_eval[0]
                run_eval = run_eval[1:]
            out["executable"] = run_eval[0]
            out["arguments"] = run_eval[1:]
        else:
            run_split: List = command.split(" ", 1)
            if run_split[0].startswith("--"):
                out["docker_syntax"] = run_split[0]
                run_split: List = run_split[1].split(" ", 1)
            if len(run_split) == 1:
                out["executable"] = run_split[0]
            else:
                out["executable"] = run_split[0]
                out["arguments"] = run_split[1]

        return out

    @staticmethod
    def _parse_multi_var(command, key_name):
        if "=" in command:
            env_split = command.split("=")
            return {key_name: env_split[0], 'default_value': env_split[1].strip("'").strip('"')}
        elif " " in command:
            env_split = command.split(" ", 1)
            return {key_name: env_split[0], 'default_value': env_split[1].strip("'").strip('"')}
        else:
            return {key_name: command}

    def _parse_dynamic_files(self, source_locations: list) -> List:
        to_copy_files = []
        for source_location in source_locations:
            if os.path.isfile(path=source_location):
                to_copy_files.extend([source_location])
                continue
            elif source_location.startswith("http"):
                continue
            ignored_files = []
            copy_files = glob.glob(f"./{source_location}/**", recursive=True)

            for pattern in self.docker_ignore_files:
                ignored_files.extend(fnmatch.filter(names=copy_files, pat=f"*{pattern}*"))
            to_copy_files.extend([i.split("./", 1)[1] for i in copy_files if i not in ignored_files and
                                  not i.endswith(f"{source_location}/")])
        return sorted(to_copy_files)

    def _parse_command(self, instruction: str, command: str) -> [Dict, List]:
        instruction = instruction.upper()
        if instruction == "COMMENT":
            comment = command.strip()
            if comment.startswith("#"):
                comment = comment.replace("#", "")
            return dict(comment=comment.strip())
        elif instruction.rstrip() == "":
            pass
        elif instruction.startswith("{%"):
            pass
        elif instruction == "FROM":
            image = dict(image=command)
            if " as " in command.lower():
                split = image["image"].lower().split(" as ")
                image["image"] = split[0]
                image["alias"] = split[1]
            if ":" in image["image"]:
                split = image["image"].split(":")
                image["image"] = split[0]
                image["version"] = split[1]
            return image
        elif instruction in ["COPY", "ADD"]:
            copy_split = command.split(" ")
            copy_dict = {}
            if copy_split[0].startswith("--chown"):
                copy_dict["chown"] = copy_split[0].split("=", 1)[1]
                copy_split = copy_split[1:]
            if len(copy_split) > 2:
                copy_dict["source"] = copy_split[:-1]
                copy_dict["parsed_source_files"] = self._parse_dynamic_files(source_locations=copy_split[:-1])
                copy_dict["target"] = copy_split[-1]
            else:
                copy_dict["source"] = [copy_split[0]]
                copy_dict["parsed_source_files"] = self._parse_dynamic_files(source_locations=[copy_split[0]])
                copy_dict["target"] = copy_split[1]
            return copy_dict
        elif instruction == "USER":
            if ":" in command:
                user_split = command.split(":")
                return dict(user=user_split[0], group=user_split[1])
            else:
                return dict(user=command)
        elif instruction == "ARG":
            if "=" in command:
                arg_split = command.split("=")
                return dict(argument=arg_split[0], default_value=arg_split[1])
            else:
                return dict(argument=command)
        elif instruction in ["ENV", "LABEL"]:
            envs = []
            if sum(i == "=" for i in command) > 1:
                for i in command.split(" "):
                    envs.append(self._parse_multi_var(command=i, key_name=instruction.lower()))
            else:
                envs.append(self._parse_multi_var(command=command, key_name=instruction.lower()))
            return envs
        elif instruction in ["RUN", "ENTRYPOINT", "CMD", "SHELL"]:
            return self._parse_json_notation(command=command)
        elif instruction == "EXPOSE":
            if "/" in command:
                expose_split = command.split("/")
                return dict(port=expose_split[0], protocol=expose_split[1])
            return dict(port=command)
        elif instruction in ["WORKDIR", "STOPSIGNAL", "VOLUME"]:
            return {instruction.lower(): command}
        elif instruction == "ONBUILD":
            command_split = command.replace(instruction, "").strip()
            command_split = self._parse_json_notation(command=command_split)
            return {
                "sub_instruction": command_split['executable'],
                **self._parse_json_notation(command=command_split['arguments'])
            }
        elif instruction == "HEALTHCHECK":
            pattern = r"--(interval|timeout|start-period|retries)=+[a-z,0-9]+"
            options = {i.group(0).replace("--", "").split("=")[0]: i.group(0).split("=", 1)[1] for i in
                       re.finditer(pattern=pattern, string=command, flags=re.MULTILINE)}

            command_split = re.sub(pattern=pattern, repl="", string=command.replace(instruction, "").strip())
            command_split = self._parse_json_notation(command=command_split.strip())
            return {
                "sub_instruction": command_split['executable'],
                "options": options,
                **self._parse_json_notation(command=command_split['arguments'])
            }
        elif instruction == "MAINTAINER":
            return dict(maintainer=command)
        else:
            raise ParsingError()

    @staticmethod
    def _concat_multi_line_instruction(lines: list) -> str:
        single_line = ""
        for i in lines:
            single_line += i["raw_command"]

        lines[0]["state"] = "multi_line_command"
        lines[0]["line_number"]["end"] = max([i["line_number"]["start"] for i in lines])
        lines[0]["raw_command"] = single_line
        return lines[0]

    def split_multi_lines(self, lines: list) -> List:
        result = []
        start_index = 0
        for i, x in enumerate(lines):
            if x["state"] == "end_multi_line_command":
                result.append(self._concat_multi_line_instruction(lines=lines[start_index:i + 1]))
                start_index = i+1
        return result

    @staticmethod
    def format_and_correct_sh(instruction, raw_command: str, raw_line):
        if instruction in ["RUN", "LABEL", "ENV"]:
            command = "{} {}\n".format(instruction, raw_command.replace('\\', '\\\n\t'))
        else:
            command = f"{raw_line}\n"

        return command

    @staticmethod
    def _get_index(li, index, offset, error_value=None):
        try:
            index = index + offset
            return li[index]
        except IndexError:
            return error_value

    def parse_dockerfile(self) -> List[dict]:
        parsed = [{"line_number": dict(start=line_number + 1, end=line_number + 1),
                   "raw_line": i,
                   "state": self._get_state(line=i),
                   "instruction": self._get_instruction(line=i.strip()),
                   "raw_command": self._get_raw_command(line=i)
                   }
                  for line_number, i in enumerate(self.df_content)]

        for i, instruction in enumerate(parsed):
            next_instruction = self._get_index(li=parsed, index=i, offset=1, error_value={})
            prev_instruction = self._get_index(li=parsed, index=i, offset=-1, error_value={})
            if instruction["state"] == "comment":
                if "continued_" in next_instruction.get("state", "") or \
                        "continued_" in prev_instruction.get("state", ""):
                    parsed[parsed.index(instruction)]["state"] = ""

        multi_line_instructions = self.split_multi_lines([i for i in parsed if "_multi_line_" in i["state"]])
        single_line_instructions = sorted(
            [i for i in parsed if i["state"] in ["new_command", "comment"]] + multi_line_instructions,
            key=lambda d: d['line_number']['start']
        )
        enriched = [dict(
                         line_number=i["line_number"],
                         instruction=i["instruction"],
                         instruction_details=self._parse_command(instruction=i["instruction"],
                                                                 command=i["raw_command"]),
                         _raw=f'{i["instruction"]} {i["raw_command"]}',
                         formatted=self.format_and_correct_sh(instruction=i['instruction'],
                                                              raw_command=i['raw_command'], raw_line=i["raw_line"])
                         )
                    for i in single_line_instructions]
        return enriched

    def _get_instructions(self, instruction: str) -> List[dict]:
        return [i for i in self.df_ast if i["instruction"] == instruction]

    @property
    def users(self) -> List[dict]:
        return self._get_instructions(instruction="USER")

    @property
    def froms(self) -> List[dict]:
        return self._get_instructions(instruction="FROM")

    @property
    def instructions(self) -> List[dict]:
        return [i["instruction"] for i in self.df_ast]

    @property
    def copies(self) -> List[dict]:
        return self._get_instructions(instruction="COPY")

    @property
    def adds(self) -> List[dict]:
        return self._get_instructions(instruction="ADD")

    @property
    def comments(self) -> List[dict]:
        return self._get_instructions(instruction="COMMENT")

    @property
    def args(self) -> List[dict]:
        return self._get_instructions(instruction="ARG")

    @property
    def envs(self) -> List[dict]:
        return self._get_instructions(instruction="ENV")

    @property
    def labels(self) -> List[dict]:
        return self._get_instructions(instruction="LABEL")

    @property
    def runs(self) -> List[dict]:
        return self._get_instructions(instruction="RUN")

    @property
    def entrypoints(self) -> List[dict]:
        return self._get_instructions(instruction="ENTRYPOINT")

    @property
    def cmds(self) -> List[dict]:
        return self._get_instructions(instruction="CMD")

    @property
    def shells(self) -> List[dict]:
        return self._get_instructions(instruction="SHELL")

    @property
    def exposes(self) -> List[dict]:
        return self._get_instructions(instruction="EXPOSE")

    @property
    def workdirs(self) -> List[dict]:
        return self._get_instructions(instruction="WORKDIR")

    @property
    def stopsignals(self) -> List[dict]:
        return self._get_instructions(instruction="STOPSIGNAL")

    @property
    def volumes(self) -> List[dict]:
        return self._get_instructions(instruction="VOLUME")

    @property
    def healthchecks(self) -> List[dict]:
        return self._get_instructions(instruction="HEALTHCHECK")

    @property
    def onbuilds(self) -> List[dict]:
        return self._get_instructions(instruction="ONBUILD")

    @property
    def maintainers(self) -> List[dict]:
        return self._get_instructions(instruction="MAINTAINER")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dockerfile", dest="dockerfile", required=False, help="Path to Dockerfile location")
    args = parser.parse_args()
    parser = DockerfileParser(dockerfile=args.dockerfile)
    print(parser.df_ast)
