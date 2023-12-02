import { mount } from "@vue/test-utils";
import { expect, test } from "vitest";
import SampleIcon from "@/components/icons/SampleIcon.vue";

test("render icon", () => {
  const icon = mount(SampleIcon, {
    props: {
      name: "alert",
    },
  });

  const SVGICON = icon.find('[data-test="alert"]');

  expect(SVGICON.exists()).toBe(true);
});

test.only("render non-existent icon", () => {
  const icon = mount(SampleIcon, {
    props: {
      name: "nonExistentIconName",
    },
  });

  expect(icon.html()).toBe("<div></div>");
});
