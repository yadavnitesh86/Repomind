def print_interrupt_summary(interrupt):
    value = interrupt.value

    action_requests = value.get("action_requests", [])

    print("\n⚠️ Approval required")

    for index, action in enumerate(action_requests, start=1):
        name = action.get("name", "Unknown tool")
        args = action.get("args", {})

        print(f"\nAction {index}: {name}")

        # For edit_file, don't print the complete file content
        if name == "edit_file":
            edits = args.get("edits", [])

            print(f"Edits: {len(edits)}")

            for edit_index, edit in enumerate(edits, start=1):
                old_text = edit.get("oldText", "")
                new_text = edit.get("newText", "")

                print(f"\nEdit {edit_index}:")
                print(f"  Old text: {len(old_text)} characters")
                print(f"  New text: {len(new_text)} characters")

                # Small preview only
                preview = new_text[:150].replace("\n", " ")
                if len(new_text) > 150:
                    preview += "..."

                print(f"  Preview: {preview}")

        else:
            # For other tools, print normal arguments
            print("Arguments:")

            for key, value in args.items():
                value_str = str(value)

                # Prevent huge output
                if len(value_str) > 300:
                    value_str = value_str[:300] + "..."

                print(f"  {key}: {value_str}")